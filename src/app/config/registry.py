from src.app.config.enums import AgentType
from src.app.config.prompts.shared import (
    PYTHON_EXPERT_SYSTEM_PROMPT,
    PYTHON_EXPERT_HUMAN_PROMPT,
    TOOL_USAGE_DECISION_SYSTEM_PROMPT,
    TOOL_USAGE_DECISION_HUMAN_PROMPT,
    TOOL_EXECUTOR_AGENT_PROMPT,
    TOOL_SELECTION_SYSTEM_PROMPT,
    TOOL_SELECTION_HUMAN_PROMPT,
    FEEDBACK_PLANNER_SYSTEM_PROMPT,
    FEEDBACK_PLANNER_HUMAN_PROMPT,
)
from src.app.config.prompts.smart_home import (
    SMART_HOME_PLAN_SYSTEM_PROMPT,
    SMART_HOME_PLAN_HUMAN_PROMPT,
    SMART_HOME_REPLANNER_SYSTEM_PROMPT,
    SMART_HOME_REPLANNER_HUMAN_PROMPT,
)
from src.app.config.prompts.web_browse import (
    WEB_BROWSE_PLAN_SYSTEM_PROMPT,
    WEB_BROWSE_REPLANNER_SYSTEM_PROMPT,
    WEB_BROWSE_REPLANNER_HUMAN_PROMPT,
)

AGENT_PROMPT_CONFIG = {
    AgentType.GENERAL_ASSISTANT: {
        "planner_prompt": {
            "system_prompt": WEB_BROWSE_PLAN_SYSTEM_PROMPT,
            "human_prompt": "{task}"
        },
        "replanner_prompt": {
            "system_prompt": WEB_BROWSE_REPLANNER_SYSTEM_PROMPT,
            "human_prompt": WEB_BROWSE_REPLANNER_HUMAN_PROMPT
        }
    },
    AgentType.SMART_HOME: {
        "planner_prompt": {
            "system_prompt": SMART_HOME_PLAN_SYSTEM_PROMPT,
            "human_prompt": SMART_HOME_PLAN_HUMAN_PROMPT
        },
        "replanner_prompt": {
            "system_prompt": SMART_HOME_REPLANNER_SYSTEM_PROMPT,
            "human_prompt": SMART_HOME_REPLANNER_HUMAN_PROMPT
        }
    },
}

COMMON_PROMPT_CONFIG = {
    "possible_tool": {
        "system_prompt": TOOL_USAGE_DECISION_SYSTEM_PROMPT,
        "human_prompt": TOOL_USAGE_DECISION_HUMAN_PROMPT
    },
    "python_expert": {
        "system_prompt": PYTHON_EXPERT_SYSTEM_PROMPT,
        "human_prompt": PYTHON_EXPERT_HUMAN_PROMPT
    },
    "tool_executor_agent_prompt": {
        "system_prompt": TOOL_EXECUTOR_AGENT_PROMPT,
    },
    "candidate_picker_chain": {
        "system_prompt": TOOL_SELECTION_SYSTEM_PROMPT,
        "human_prompt": TOOL_SELECTION_HUMAN_PROMPT
    },
    "plan_via_feedback": {
        "system_prompt": FEEDBACK_PLANNER_SYSTEM_PROMPT,
        "human_prompt": FEEDBACK_PLANNER_HUMAN_PROMPT
    }
}