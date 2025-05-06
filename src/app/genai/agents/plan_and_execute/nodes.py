from langgraph.types import interrupt
from langchain_core.runnables.config import RunnableConfig

from app.genai.agents.plan_and_execute.chains import (
    create_planner_chain,
    create_replanner_chain,
    create_feedback_planner_chain
) 
from app.genai.agents.plan_and_execute.schemas import (
    Plan,
    PlanExecute,
    Act,
    Response,
    ReviewPlan,
    PlanToReview
)
from app.genai.agents.tool_manipulator.agent import agent_tool_manipulator
from app.genai.agents.tool_manipulator.schemas import AgentState
from app.config.enums import AgentType, PlanReviewAction, PlanReviewType


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
            agent_type=agent_type,
            past_steps=state.past_steps)
    )
    new_past_steps = list(state.past_steps or [])
    new_past_steps.append((task, agent_response["answer"]))

    return PlanExecute(
        task=state.task,
        plan=state.plan,
        past_steps=new_past_steps,
    )


def human_plan_revision(state: PlanExecute) -> PlanExecute:
    print("HUMAN REVIEW PLAN")
    value: ReviewPlan = interrupt(
        PlanToReview(
            task=state.task,
            plan_to_review=state.plan.steps
        )
    )
    print("HUMAN REVIEWED PLAN")

    if value.action == PlanReviewAction.APPROVE:
        print("APPROVED")
        return state.model_copy(
            update={
                "next_node": "execute_step"
            },
        )
    elif value.action == PlanReviewAction.MODIFY:
        return state.model_copy(
            update={
                "plan": Plan(
                    steps=value.steps
                ),
                "next_node": "execute_step"
            }
        )
    elif value.action == PlanReviewAction.FEEDBACK:
            return state.model_copy(
                update={
                    "feedback": value.feedback,
                    "next_node": "plan_with_feedback"
                }
            )


def plan_step(state: PlanExecute, config: RunnableConfig) -> PlanExecute:
    print("PLANNING")
    agent_type: AgentType = config["configurable"].get("agent_type")
    
    prompt_input = {
        "task": state.task
    }

    chain = create_planner_chain(agent_type)
    plan: Plan = chain.invoke(prompt_input)
    return state.model_copy(
        update={
            "plan": plan,
            "feedback_type": PlanReviewType.PLAN,
        }
    )


def replan_step(state: PlanExecute, config: RunnableConfig) -> PlanExecute:
    print("REPLANNING")
    agent_type: AgentType = config["configurable"].get("agent_type")
    chain = create_replanner_chain(agent_type)
    output: Act = chain.invoke({
        "task": state.task,
        "plan": state.plan,
        "past_steps": state.past_steps
    })
    

    if isinstance(output.action, Response):
        return state.model_copy(
            update={
                "response": output.action.response,
                "next_node": "final_answer"
            },
        )
    else:
        return state.model_copy(
            update={
                "plan": output.action,
                "feedback_type": PlanReviewType.REPLAN,
                "next_node": "human_plan_review",
            },
        )


def plan_with_feedback(state: PlanExecute) -> PlanExecute:
    chain = create_feedback_planner_chain()
    print("PLANNING WITH FEEDBACK")
    # print(state)

    prompt_input = {
        "task": state.task,
        "previous_plan": "\n".join(state.plan.steps),
        "feedback": state.feedback
    }

    updated_plan: Plan = chain.invoke(prompt_input)

    return state.model_copy(
        update={
            "plan": updated_plan,
            "next_node": "human_plan_review",
        }
    )


def final_answer(state: PlanExecute) -> PlanExecute:
    return state
