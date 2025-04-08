from src.app.config.enums import AgentType
from app.config.prompts.smart_home import (
    PYTHON_EXPERT_SYSTEM_PROMPT,
    PYTHON_EXPERT_HUMAN_PROMPT,
    SMART_HOME_PLAN_SYSTEM_PROMPT,
    SMART_HOME_REPLANNER_SYSTEM_PROMPT,
    SMART_HOME_REPLANNER_HUMAN_PROMPT,
    HOME_SMART_TOOL_SELECTOR_SYSTEM_PROMPT,
)

AGENT_PROMPT_CONFIG = {
    AgentType.SMART_HOME: {
        "selector_chain": {
            "system_prompt": HOME_SMART_TOOL_SELECTOR_SYSTEM_PROMPT
        },
        "python_expert": {
            "system_prompt": PYTHON_EXPERT_SYSTEM_PROMPT,
            "human_prompt": PYTHON_EXPERT_HUMAN_PROMPT
        },
        "tool_executor_agent_prompt": {
            "system_prompt": "You are a helpful assistant that uses provided tools to directly perform tasks.",
            "human_prompt": "{input}",
            "placeholder": "{agent_scratchpad}"
        },
        "planner_prompt": {
            "system_prompt": SMART_HOME_PLAN_SYSTEM_PROMPT,
            "human_prompt": "{task}"
        },
        "replanner_prompt": {
            "system_prompt": SMART_HOME_REPLANNER_SYSTEM_PROMPT,
            "human_prompt": SMART_HOME_REPLANNER_HUMAN_PROMPT
        }
    },
    # Add SCHEDULING_ASSISTANT and GENERAL_ASSISTANT here...
}