from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_core.runnables import RunnableConfig
from langgraph.func import entrypoint



@entrypoint(checkpointer=MemorySaver())
async def chatbot(input: MessagesState, config: RunnableConfig):
    