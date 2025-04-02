from pydantic import BaseModel, Field
from typing import List, Tuple


class BaseTaskState(BaseModel):
    task: str


class Plan(BaseTaskState):
    steps: List[str] = Field(
        description="Different steps to follow, should be in sorted order"
    )


class PlanExecute(BaseTaskState):
    plan: Plan
    past_steps: List[Tuple] = Field(
        description="List of steps and their corresponding outputs"
    )


class Response(BaseModel):
    response: str


class Act(BaseModel):
    action: Response | Plan = Field(
        description="Action to perform. If you want to respond to user, use Response. \
        If you need to further use tools to get the answer, use Plan."
    )


