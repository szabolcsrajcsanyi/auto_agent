from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

from app.genai.agents.plan_and_execute.schemas import Plan, Act
from app.config.registry import AGENT_PROMPT_CONFIG, COMMON_PROMPT_CONFIG
from app.config.enums import AgentType
from app.genai.llm import llm


def create_planner_chain(agent_type: AgentType):
        planner_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=AGENT_PROMPT_CONFIG[agent_type]["planner_prompt"]["system_prompt"]),
                ("human", AGENT_PROMPT_CONFIG[agent_type]["planner_prompt"]["human_prompt"]),
        ])
        return planner_prompt | llm.with_structured_output(Plan)


def create_replanner_chain(agent_type: AgentType):
        replanner_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=AGENT_PROMPT_CONFIG[agent_type]["replanner_prompt"]["system_prompt"]),
                ("human", AGENT_PROMPT_CONFIG[agent_type]["replanner_prompt"]["human_prompt"]),
        ])
        return replanner_prompt | llm.with_structured_output(Act)


def create_feedback_planner_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", COMMON_PROMPT_CONFIG["plan_via_feedback"]["system_prompt"]),
        ("human", COMMON_PROMPT_CONFIG["plan_via_feedback"]["human_prompt"]),
    ])
    return prompt | llm.with_structured_output(Plan)