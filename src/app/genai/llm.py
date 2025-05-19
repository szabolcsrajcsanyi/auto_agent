from typing import List
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent


llm = ChatOpenAI(
    model="gpt-4.1-mini", temperature=0
)


tool_answer_llm = ChatOpenAI(
    model="gpt-4.1-mini", temperature=1
)


tool_generate_llm = ChatOpenAI(
    model="o4-mini"
)


def create_agent_executor_with_tools(tools: List[BaseTool]):
    return create_react_agent(
        model=tool_answer_llm, 
        tools=tools, 
        prompt="You are a helpful assistant that uses provided tools to directly perform tasks."
    )
