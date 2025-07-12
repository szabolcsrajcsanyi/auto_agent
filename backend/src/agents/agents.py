from dataclasses import dataclass
from langgraph.pregel import Pregel
from chatbot import chatbot


DEFAULT_AGENT = "chatbot"


@dataclass
class Agent:
    description: str
    graph: Pregel


agents: dict[str, Agent] = {
    "chatbot": Agent(
        description="A simple chatbot agent that responds to user messages.",
        graph=chatbot
    )
}


def get_agent(agent_id: str) -> Pregel:
    return agents[agent_id].graph
