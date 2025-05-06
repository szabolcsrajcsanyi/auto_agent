from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Tuple

from app.config.enums import AgentType, CodeReviewAction


class BaseTaskState(BaseModel):
    task: str


class CandidateTool(BaseModel):
    tool_choice: Literal["1", "2", "3", "NONE"]
    reason: Optional[str] = None


class ToolSelection(BaseModel):
    needs_tool: Optional[bool] = None
    tool_description: Optional[str] = None


class ToolData(BaseModel):
    retrieved_tool_ids: List[str] = []
    candidate_tool: Optional[str] = None
    reason: Optional[str] = None
    tool_output: Optional[str] = None


class CodeFeedback(BaseModel):
    code: Optional[str] = None
    feedback: Optional[str] = None


class AgentState(BaseTaskState):
    past_steps: Optional[List[Tuple]] = Field(
        default=None,
        description="List of steps and their corresponding outputs"
    )
    agent_type: AgentType = AgentType.SMART_HOME # Default agent type

    # Tool logic
    tool_selection: ToolSelection = ToolSelection()
    tool_data: ToolData = ToolData()
    tool_feedback: CodeFeedback = CodeFeedback()

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
    feedback: Optional[str] = None
    action: Optional[CodeReviewAction] = None
    

class EvaluationResult(BaseModel):
    success: bool
    reason: str
    