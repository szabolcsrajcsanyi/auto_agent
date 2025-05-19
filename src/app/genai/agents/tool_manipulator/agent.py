from langgraph.graph import StateGraph, END
from app.genai.agents.tool_manipulator.schemas import (
    AgentState,
)
from app.genai.agents.tool_manipulator.nodes import (
    answer_with_selected_tool,
    answer_without_tool,
    decide_candidate_tool,
    decide_tool_use,
    evalutate_tool_outcome,
    generate_tool,
    human_supervision,
    register_tool,
    retrieve_candidate_tools
)


# Initialize the StateGraph with the initial state
graph_builder = StateGraph(
    state_schema=AgentState,
)


# Define nodes
graph_builder.add_node("decide_tool_use", decide_tool_use)
graph_builder.add_node("retrieve_tools", retrieve_candidate_tools)
graph_builder.add_node("decide_candidate_tool", decide_candidate_tool)
graph_builder.add_node("answer_with_tool", answer_with_selected_tool)
graph_builder.add_node("evaluate_tool_outcome", evalutate_tool_outcome)
graph_builder.add_node("answer_without_tool", answer_without_tool)
graph_builder.add_node("generate_tool", generate_tool)
graph_builder.add_node("human_supervision", human_supervision)
graph_builder.add_node("register_tool", register_tool)


# Set entry point
graph_builder.set_entry_point("decide_tool_use")


# Normal transitions
graph_builder.add_conditional_edges(
    "decide_tool_use",
    lambda state: state.next_node,
    ["retrieve_tools", "answer_without_tool"]
)
graph_builder.add_conditional_edges(
    "retrieve_tools",
    lambda state: state.next_node,
    ["decide_candidate_tool", "generate_tool"]
)
graph_builder.add_conditional_edges(
    "decide_candidate_tool",
    lambda state: state.next_node,
    ["answer_with_tool", "generate_tool"]
)
graph_builder.add_edge("generate_tool", "human_supervision")
graph_builder.add_conditional_edges(
    "human_supervision",
    lambda state: state.next_node,
    ["register_tool", "generate_tool"]
)
graph_builder.add_edge("register_tool", "answer_with_tool")
graph_builder.add_edge("answer_with_tool", "evaluate_tool_outcome")
graph_builder.add_conditional_edges(
    "evaluate_tool_outcome",
    lambda state: state.next_node,
    ["decide_candidate_tool", "generate_tool", END]
)
graph_builder.add_edge("answer_without_tool", END)


# Compile the graph
agent_tool_manipulator = graph_builder.compile()
