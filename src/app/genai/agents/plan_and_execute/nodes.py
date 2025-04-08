from typing import Literal
from langgraph.types import Command, interrupt
from langgraph.graph import END
from langchain_core.runnables.config import RunnableConfig

from src.app.genai.agents.plan_and_execute.chains import (
    create_planner_chain,
    create_replanner_chain
) 
from src.app.genai.agents.plan_and_execute.schemas import (
    Plan,
    PlanExecute,
    Act,
    Response,
    ReviewPlan,
    PlanToReview
)
from src.app.genai.agents.tool_manipulator.agent import agent_tool_manipulator
from src.app.genai.agents.tool_manipulator.schemas import BaseTaskState, AgentState
from src.app.config.enums import AgentType, PlanReviewAction


def execute_step(state: PlanExecute, config: RunnableConfig) -> PlanExecute:
    print("EXECUTING")
    agent_type: AgentType = config["configurable"].get("agent_type")
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(state.plan.steps))
    task = state.plan.steps[0]
    task_formatted = f"""For the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    agent_response = agent_tool_manipulator.invoke(
        AgentState(
            task=task_formatted,
            agent_type=agent_type)
    )
    print("EXECUTED")
    return PlanExecute(
        task=task,
        plan=state.plan,
        past_steps=[(task, agent_response["answer"])],
    )


def human_plan_revision(state: PlanExecute) -> PlanExecute:
    value: ReviewPlan = interrupt(
        PlanToReview(
            task=state.task,
            plan_to_review=state.plan.steps
        )
    )

    if value.action == PlanReviewAction.APPROVE:
        return PlanExecute(
            task=state.task,
            plan=state.plan,
            next_node="execute_step"
        )
    elif value.action == PlanReviewAction.MODIFY:
        return PlanExecute(
            task=state.task,
            plan=Plan(
                task=state.task,
                steps=value.steps
            ),
            next_node="execute_step"
        )
    elif value.action == PlanReviewAction.FEEDBACK:
        return PlanExecute(
            task=value.feedback,
            next_node="planner"
        )


def plan_step(state: PlanExecute, config: RunnableConfig) -> PlanExecute:
    print("PLANNING")
    agent_type: AgentType = config["configurable"].get("agent_type")
    chain = create_planner_chain(agent_type)
    plan: Plan = chain.invoke(("task", state.task))
    return PlanExecute(
        task=plan.task,
        plan=plan,
    )


def replan_step(state: PlanExecute, config: RunnableConfig) -> Command[Literal["execute_step"]]:
    print("REPLANNING")
    agent_type: AgentType = config["configurable"].get("agent_type")
    chain = create_replanner_chain(agent_type)
    output: Act = chain.invoke({
        "task": state.task,
        "plan": state.plan,
        "past_steps": state.past_steps
    })
    if isinstance(output.action, Response):
        return Command(
            update=output.action.response,
            goto=END
        )
    else:
        return Command(
            update=output.action,
            goto="execute_step"
        )
