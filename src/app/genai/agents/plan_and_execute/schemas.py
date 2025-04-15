from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

from src.app.config.enums import PlanReviewAction, PlanReviewType


class Plan(BaseModel):
    steps: Optional[List[str]] = Field(
        default=None,
        description="Different steps to follow, should be in sorted order"
    )


class Response(BaseModel):
    response: str


class Act(BaseModel):
    action: Optional[Response | Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. \
        If you need to further use tools to get the answer, use Plan."
    )


class PlanExecute(BaseModel):
    task: str
    past_steps: Optional[List[Tuple]] = Field(
        default=None,
        description="List of steps and their corresponding outputs"
    )

    plan: Plan = Plan()
    feedback: Optional[str] = None
    feedback_type: Optional[PlanReviewType] = None
    response: Optional[str] = None
    next_node: Optional[str] = None


class ReviewPlan(BaseModel):
    action: PlanReviewAction
    steps: Optional[List[str]] = None
    feedback: Optional[str] = None


class PlanToReview(BaseModel):
    task: str
    plan_to_review: List[str] = Field(
        description="Plan to review. Should be in sorted order"
    )
    

class PlanFeedback(BaseModel):
    task: str
    feedback: str
    plan_to_review: List[str] = Field(
        description="Plan to review. Should be in sorted order"
    )
    