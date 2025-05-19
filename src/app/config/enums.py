from enum import Enum


class AgentType(str, Enum):
    GENERAL_ASSISTANT = "general_assistant"
    SMART_HOME = "smart_home"
    SHOPPING_HISTORY = "shopping_history"
    INVENTORY_MANAGEMENT = "inventory_management"


class PlanReviewAction(str, Enum):
    APPROVE = "approve"
    MODIFY = "modify"
    FEEDBACK = "feedback"


class CodeReviewAction(str, Enum):
    APPROVE = "approve"
    FEEDBACK = "feedback"
    

class PlanReviewType(str, Enum):
    PLAN = "plan"
    REPLAN = "replan"
    