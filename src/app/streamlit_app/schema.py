from pydantic import BaseModel, Field
from langgraph.types import Interrupt
from typing import Literal, List, Optional, Tuple

from app.genai.agents.plan_and_execute.schemas import (
    PlanExecute,
    Response
)
from app.genai.agents.tool_manipulator.schemas import (
    AgentState
)


class ChatMessage(BaseModel):
    type: Literal["human", "ai"]
    content: List[str]
    past_steps: List[str] = None
    state: AgentState | PlanExecute | Tuple[Interrupt] = None
    node: str = None


class StreamOutput(BaseModel):
    planner: Optional[PlanExecute] = None
    replanner: Optional[PlanExecute] = None
    execute_step: Optional[PlanExecute] = None
    final_answer: Optional[PlanExecute] = None
    human_plan_review: Optional[Tuple[Interrupt]] = Field(default=None, alias="__interrupt__")
    plan_with_feedback: Optional[PlanExecute] = None
    decide_tool_use: Optional[AgentState] = None
    retrieve_tools: Optional[AgentState] = None
    decide_candidate_tool: Optional[AgentState] = None
    generate_tool: Optional[AgentState] = None
    answer_with_tool: Optional[AgentState] = None
    evaluate_tool_outcome: Optional[AgentState] = None
    answer_without_tool: Optional[AgentState] = None
    