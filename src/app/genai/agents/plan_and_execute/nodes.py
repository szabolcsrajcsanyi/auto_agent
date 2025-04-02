from typing import Literal, Generator
from langgraph.types import Command
from langgraph.graph import END

from src.app.genai.agents.plan_and_execute.chains import planner, replanner
from src.app.genai.agents.plan_and_execute.schemas import (
    BaseTaskState, 
    Plan, 
    PlanExecute,
    Act,
    Response
)
from src.app.genai.agents.tool_manipulator.agent import agent_tool_manipulator
from src.app.genai.agents.tool_manipulator.schemas import BaseTaskState, AgentState


def execute_step(state: Plan) -> PlanExecute:
    print("EXECUTING")
    plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(state.steps))
    task = state.steps[0]
    task_formatted = f"""For the following plan:
{plan_str}\n\nYou are tasked with executing step {1}, {task}."""
    agent_response = agent_tool_manipulator.invoke(
        AgentState(task=task_formatted)
    )
    print(agent_response)
    print("EXECUTED")
    return PlanExecute(
        task=task,
        plan=state,
        past_steps=[(task, agent_response["answer"])],
    )


def plan_step(state: BaseTaskState) -> Plan:
    print("PLANNING")
    plan: Plan = planner.invoke(("task", state.task))
    return Plan(
        task=plan.task,
        steps=plan.steps
    )


def replan_step(state: PlanExecute) -> Command[Literal["execute_step"]]:
    print("REPLANNING")
    output: Act = replanner.invoke({
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
