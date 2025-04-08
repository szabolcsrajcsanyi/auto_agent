from pydantic import BaseModel
from typing import List, Optional

from src.app.config.enums import AgentType


class BaseTaskState(BaseModel):
    task: str


class ToolSelection(BaseModel):
    needs_tool: Optional[bool] = None
    tool_description: Optional[str] = None


class ToolData(BaseModel):
    retrieved_tool_ids: List[str] = []
    tool_output: Optional[str] = None


class AgentState(BaseTaskState):
    task: str
    agent_type: AgentType = AgentType.SMART_HOME # Default agent type

    # Tool logic
    tool_selection: ToolSelection = ToolSelection()
    tool_data: ToolData = ToolData()

    next_node: Optional[str] = None

    answer: Optional[str] = None


class ToolDecisionState(BaseTaskState):
    needs_tool: bool
    tool_description: str | None


class ToolExpert(BaseModel):
    task: str
    tool_output: str


class RetrieveToolState(BaseModel):
    task: str
    retrieved_tool_ids: List[str] = []


class ReviewCode(BaseModel):
    code: str
    