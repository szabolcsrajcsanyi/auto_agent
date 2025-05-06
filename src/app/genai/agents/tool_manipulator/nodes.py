from langgraph.types import interrupt
from langgraph.graph import END
from langchain_core.runnables.config import RunnableConfig

from app.genai.agents.tool_manipulator.schemas import (
    ToolDecisionState, 
    AgentState,
    ToolSelection,
    CandidateTool,
    ToolData,
    ReviewCode,
    CodeFeedback,
    EvaluationResult
)
from app.genai.agents.tool_manipulator.chains import (
    candidate_picker_chain,
    determin_possible_tool_chain,
    python_expert_chain,
    tool_evaluator_chain
)
from app.genai.llm import llm, create_agent_executor_with_tools
from app.genai.tools.tool_manager import ToolManager
from app.config.enums import CodeReviewAction


def decide_tool_use(state: AgentState) -> AgentState:
    print("DECIDE TOOL USE")
    chain = determin_possible_tool_chain()
    decision: ToolDecisionState = chain.invoke({"task": state.task})
    state = state.model_copy(
        update={
            "tool_selection": ToolSelection(
                needs_tool=decision.needs_tool, 
                tool_description=decision.tool_description
            )
        }
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
    

def retrieve_candidate_tools(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
    candidate_tool_ids = tool_manager.find_best_tool(state.tool_selection.tool_description)

    if not candidate_tool_ids:
        return state.model_copy(
            update={
                "next_node": "generate_tool"
            }
        )
    else:
        return state.model_copy(
            update={
                "tool_data": ToolData(
                    retrieved_tool_ids=candidate_tool_ids,
                    tool_output=None
                ),
                "next_node": "decide_candidate_tool"
            }
        )
    

def decide_candidate_tool(state: AgentState, config: RunnableConfig) -> AgentState:
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
    tools = tool_manager.get_tools_by_ids(state.tool_data.retrieved_tool_ids)
    tool_descs = [tool.description for tool in tools]

    tools_str = "\n".join([f"{i+1}. {desc}" for i, desc in enumerate(tool_descs)])

    past_steps_str = "\n".join(
        [f"{i+1}. {step[0]}\n{step[1]}" for i, step in enumerate(state.past_steps)]
    ) if hasattr(state, "past_steps") and state.past_steps else "None"

    chain = candidate_picker_chain()
    selection: CandidateTool = chain.invoke({
        "task": state.task,
        "tools": tools_str,
        "past_steps": past_steps_str,
    })
    print(selection)

    if selection.tool_choice in {"1", "2", "3"}:
        selected_index = int(selection.tool_choice) - 1
        selected_tool_id = state.tool_data.retrieved_tool_ids[selected_index]
        return state.model_copy(
            update={
                "tool_data": ToolData(
                    candidate_tool=selected_tool_id,
                    reason=selection.reason,
                    tool_output=None
                ),
                "next_node": "answer_with_tool"
            }
        )
    else:
        return state.model_copy(
                update={
                    "next_node": "generate_tool"
                }
            )


def generate_tool(state: AgentState) -> AgentState:
    past_steps_str = "\n".join(
        [f"{i+1}. Question: {q}\n   Answer: {a}" for i, (q, a) in enumerate(state.past_steps or [])]
    ) or "None"

    if state.tool_feedback and state.tool_data and state.tool_data.tool_output:
        prompt_input = {
            "task_description": state.task,
            "context": past_steps_str,
            "feedback": state.tool_feedback.feedback,
            "previous_code": state.tool_feedback.code
        }
    else:
        # Initial generation path
        prompt_input = {
            "task_description": state.task,
            "context": past_steps_str,
            "feedback": "None",
            "previous_code": "None"
        }

    chain = python_expert_chain()
    result = chain.invoke(prompt_input)
    return state.model_copy(
        update={
            "tool_data": ToolData(
                retrieved_tool_ids=[],
                tool_output=result.content
            )
        }
    )


def human_supervision(state: AgentState) -> AgentState:
    print("HUMAN REVIEW")
    value: ReviewCode = interrupt(
        ReviewCode(
            code=state.tool_data.tool_output,
        )
    )

    if value.action == CodeReviewAction.APPROVE:
        return state.model_copy(
            update={
                "tool_data": ToolData(
                    retrieved_tool_ids=state.tool_data.retrieved_tool_ids,
                    tool_output=value.code
                ),
                "next_node": "register_tool"
            }
        )
    else:
        return state.model_copy(
            update={
                "tool_feedback": CodeFeedback(
                    code=value.code,
                    feedback=value.feedback
                ),
                "next_node": "generate_tool"
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


def answer_with_selected_tool(state: AgentState, config: RunnableConfig) -> AgentState:
    print("ANSWER WITH TOOL")
    tool_manager: ToolManager = config["configurable"].get("tool_manager")
    tools = tool_manager.get_tools_by_ids([state.tool_data.candidate_tool])
    agent_executor = create_agent_executor_with_tools(tools)

    context_messages = []
    if state.past_steps:
        for question, answer in state.past_steps:
            context_messages.append(("user", question))
            context_messages.append(("assistant", answer))

    context_messages.append(("user", state.task))

    agent_response = agent_executor.invoke({
        "messages": context_messages,
        # "messages": [("user", state.task)]
    })
    return state.model_copy(
        update={
            "answer": agent_response["messages"][-1].content,
        }
    )


def evalutate_tool_outcome(state: AgentState) -> AgentState:
    print("EVALUATE TOOL OUTCOME")
    selected_tool_id = state.tool_data.candidate_tool
    
    evaluation_chain = tool_evaluator_chain()
    result: EvaluationResult = evaluation_chain.invoke({
        "task": state.task,
        "selection_reason": state.tool_data.reason,
        "tool_output": state.answer
    })

    if result.success:
        return state.model_copy(update={"next_node": END})
    
    remaining_ids = [
        tid for tid in state.tool_data.retrieved_tool_ids if tid != selected_tool_id
    ]

    if remaining_ids:
        return state.model_copy(
            update={
                "tool_data": ToolData(
                    retrieved_tool_ids=remaining_ids,
                    tool_output=None
                ),
                "next_node": "decide_candidate_tool"
            }
        )
    else:
        return state.model_copy(
            update={"next_node": "generate_tool"}
        )


def answer_without_tool(state: AgentState) -> AgentState:
    result = llm.invoke(state.task)
    return state.model_copy(
        update={
            "answer": result.content,
        }
    )
