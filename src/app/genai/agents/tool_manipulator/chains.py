
from langchain_core.prompts import ChatPromptTemplate

from src.app.genai.shared.llm import llm
from src.app.genai.agents.tool_manipulator.schemas import ToolDecisionState
from src.app.config.enums import AgentType
from src.app.config.registry import AGENT_PROMPT_CONFIG


def create_selector_chain(agent_type: AgentType):
    selector_prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_PROMPT_CONFIG[agent_type]["selector_chain"]["system_prompt"]),
        ("human", "{task}")
    ])
    return selector_prompt | llm.with_structured_output(ToolDecisionState)


def create_python_expert_chain(agent_type: AgentType):
    expert_prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_PROMPT_CONFIG[agent_type]["python_expert"]["system_prompt"]),
        ("human", AGENT_PROMPT_CONFIG[agent_type]["python_expert"]["human_prompt"]),
    ])
    return expert_prompt | llm


#TODO:
tool_executor_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", AGENT_PROMPT_CONFIG[AgentType.SMART_HOME]["tool_executor_agent_prompt"]["system_prompt"]),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])


# if __name__ == "__main__":
#     task = "Turn on the lights in the kitchen"
#     user_input = HUMAN.format(task_description=task)
#     result = python_expert_llm_chain.invoke({
#         "user_input": user_input
#     })

#     result.pretty_print()
