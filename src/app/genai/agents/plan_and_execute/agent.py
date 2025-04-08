from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

from src.app.genai.agents.plan_and_execute.schemas import (
    PlanExecute, 
    Response
)
from src.app.genai.agents.plan_and_execute.nodes import (
    plan_step,
    execute_step,
    replan_step,
    human_plan_revision
)


graph_builder = StateGraph(PlanExecute, output=Response)

# Add the plan node
graph_builder.add_node("planner", plan_step)
graph_builder.add_node("execute_step", execute_step)
graph_builder.add_node("replanner", replan_step)
graph_builder.add_node("human_plan_review", human_plan_revision)

graph_builder.set_entry_point("planner")

# graph_builder.add_edge("planner", "execute_step")
graph_builder.add_edge("planner", "human_plan_review")
graph_builder.add_conditional_edges(
    "human_plan_review",
    lambda state: state.next_node,
    ["planner", "execute_step"]
)
graph_builder.add_edge("execute_step", "replanner")

memory = MemorySaver()

plan_and_execute_agent = graph_builder.compile(checkpointer=memory)
