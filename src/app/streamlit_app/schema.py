from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from langgraph.types import Interrupt

from src.app.genai.agents.plan_and_execute.schemas import (
    PlanExecute,
    Plan
)
from src.app.genai.agents.tool_manipulator.schemas import (
    AgentState,
)


class StepExecutionResult(BaseModel):
    task: str
    plan: Plan
    past_steps: List[tuple]


class StreamOutput(BaseModel):
    planner: Optional[PlanExecute] = None
    execute_step: Optional[PlanExecute] = None
    human_plan_review: Optional[Tuple[Interrupt]] = Field(default=None, alias="__interrupt__")
    decide_tool_use: Optional[AgentState] = None
    retrieve_tools: Optional[AgentState] = None
    generate_tool: Optional[AgentState] = None
    answer_with_tool: Optional[AgentState] = None
    answer_without_tool: Optional[AgentState] = None
    