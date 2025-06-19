from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_core.runnables import RunnableConfig
from langgraph.func import entrypoint
from langchain_core.messages import BaseMessage


@entrypoint(checkpointer=MemorySaver())
async def chatbot(
    input: MessagesState, 
    previous: list[BaseMessage], 
    config: RunnableConfig) -> entrypoint.final[
        dict[str, list[BaseMessage]],
        dict[str, list[BaseMessage]]
    ]:
    messages = input.messages

    