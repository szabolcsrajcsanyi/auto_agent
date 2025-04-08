from langgraph.types import interrupt
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.runnables.config import RunnableConfig

from src.app.genai.agents.tool_manipulator.schemas import (
    RetrieveToolState, 
    ToolDecisionState, 
    AgentState,
    ToolSelection,
    ToolData,
    ReviewCode
)
from src.app.genai.agents.tool_manipulator.chains import (
    create_python_expert_chain, 
    create_selector_chain, 
    tool_executor_agent_prompt
)
from src.app.genai.shared.llm import llm
from src.app.genai.shared.tool_manager import ToolManager


def retrieve_tools(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
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


def answer_with_tool(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
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
    chain = create_selector_chain(state.agent_type)
    decision: ToolDecisionState = chain.invoke({"task": state.task})
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
    chain = create_python_expert_chain(state.agent_type)
    result = chain.invoke({"task_description": state.task})
    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=[],
                tool_output=result.content
            )
        }
    )


def register_tool(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
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
    print("HUMAN REVIEW")
    value = interrupt(
        ReviewCode(
            code=state.tool_data.tool_output
        )
    )

    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=state.tool_data.retrieved_tool_ids,
                tool_output=value
            )
        }
    )
