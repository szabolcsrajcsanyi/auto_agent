from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from src.app.genai.agents.plan_and_execute.schemas import Plan, Act
from src.app.genai.agents.plan_and_execute.prompts import (
        SYSTEM_PROMPT_PLAN,
        SYSTEM_PROMPT_REPLANNER,
        HUMAN_PROMPT_REPLANNER
)
from src.app.genai.shared.llm import llm


planner_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT_PLAN),
        ("human", "{task}")
])


replanner_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT_REPLANNER),
        ("human", HUMAN_PROMPT_REPLANNER)
])


planner = planner_prompt | llm.with_structured_output(Plan)
replanner = replanner_prompt | llm.with_structured_output(Act)
