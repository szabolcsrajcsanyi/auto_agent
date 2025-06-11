from dataclasses import dataclass
from langgraph.pregel import Pregel

@dataclass
class Agent:
    description: str
    graph: Pregel


agents: dict[str, Agent] = {
    "chatbot": Agent(
        description="A simple chatbot agent that responds to user messages.",
        graph=
    )
}