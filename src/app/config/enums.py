from enum import Enum

class AgentType(str, Enum):
    SMART_HOME = "smart_home"
    SCHEDULING_ASSISTANT = "scheduling_assistant"
    GENERAL_ASSISTANT = "general_assistant"


class PlanReviewAction(str, Enum):
    APPROVE = "approve"
    MODIFY = "modify"
    FEEDBACK = "feedback"
