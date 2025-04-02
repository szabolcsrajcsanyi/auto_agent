from typing import Literal
from langgraph.types import Command, interrupt
from langchain.agents import create_openai_tools_agent, AgentExecutor

from src.app.genai.agents.tool_manipulator.schemas import (
    RetrieveToolState, 
    ToolDecisionState, 
    AgentState,
    ToolSelection,
    ToolData
)
from src.app.genai.agents.tool_manipulator.chains import tool_selector_llm_chain, python_expert_llm_chain, tool_executor_agent_prompt
from src.app.genai.shared.tool_manager import tool_manager
from src.app.genai.shared.llm import llm


def retrieve_tools(state: AgentState) -> AgentState:
    tool_ids = tool_manager.find_best_tool(state.tool_selection.tool_description)
    state = AgentState(
        task=state.task,
        tool_selection=ToolSelection(
            needs_tool=state.tool_selection.needs_tool,
            tool_description=state.tool_selection.tool_description
        ),
        tool_data=ToolData(
            retrieved_tool_ids=tool_ids,
            tool_output=None
        )
    )
    if tool_ids:
        return state.model_copy(
            update={
                "next_node": "answer_with_tool"
            }
        )
    else:
        return state.model_copy(
            update={
                "next_node": "generate_tool"
            }
        )


def answer_with_tool(state: AgentState) -> AgentState:
    tools = tool_manager.get_tools_by_ids(state.tool_data.retrieved_tool_ids)
    agent = create_openai_tools_agent(llm, tools, tool_executor_agent_prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    result = executor.invoke({"input": state.task})
    return state.model_copy(
        update={
            "answer": result["output"],
        }
    )


def answer_without_tool(state: AgentState) -> AgentState:
    result = llm.invoke(state.task)
    return state.model_copy(
        update={
            "answer": result.content,
        }
    )


def decide_tool_use(state: AgentState) -> AgentState:
    decision: ToolDecisionState = tool_selector_llm_chain.invoke({"task": state.task})
    state = AgentState(
        task=state.task,
        tool_selection=ToolSelection(
            needs_tool=decision.needs_tool, 
            tool_description=decision.tool_description
        )
    )
    if decision.needs_tool:
        return state.model_copy(
            update={
                "next_node": "retrieve_tools"
            }
        )
    else:
        return state.model_copy(
            update={
                "next_node": "answer_without_tool"
            }
        )


def generate_tool(state: AgentState) -> AgentState:
    result = python_expert_llm_chain.invoke({"user_input": state.task})
    # tool_metadata, _ = tool_manager.generate_and_register_tool(result.content)
    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=[],
                tool_output=result.content
            )
        }
    )


def register_tool(state: AgentState) -> AgentState:
    tool_metadata, _ = tool_manager.generate_and_register_tool(state.tool_data.tool_output)
    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=[tool_metadata.tool_id],
                tool_output=state.tool_data.tool_output
            )
        }
    )


def human_supervision(state: AgentState) -> AgentState:
    value = interrupt(
        {
            "code_to_review": state.tool_data.tool_output
        }
    )

    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=state.tool_data.retrieved_tool_ids,
                tool_output=value
            )
        }
    )
