from pydantic import BaseModel
from typing import List, Optional

from src.app.genai.agents.plan_and_execute.schemas import Plan
from src.app.genai.agents.tool_manipulator.schemas import (
    AgentState,
)


class StepExecutionResult(BaseModel):
    task: str
    plan: Plan
    past_steps: List[tuple]


class StreamOutput(BaseModel):
    planner: Optional[Plan] = None
    decide_tool_use: Optional[AgentState] = None
    retrieve_tools: Optional[AgentState] = None
    generate_tool: Optional[AgentState] = None
    answer_with_tool: Optional[AgentState] = None
    answer_without_tool: Optional[AgentState] = None
    execute_step: Optional[StepExecutionResult] = None