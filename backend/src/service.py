from uuid import UUID, uuid4
from fastapi import FastAPI, APIRouter
from langgraph.pregel import Pregel
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

from backend.src.schema.schema import UserInput
from backend.src.core.llm import get_model
from backend.src.agents.agents import get_agent, DEFAULT_AGENT


app = FastAPI()
router = APIRouter()


@router.post("/{agent_id}/invoke")
@router.post("/invoke")
async def invoke(user_input: UserInput, agent_id: str = DEFAULT_AGENT):
    agent: Pregel = get_model(agent_id)

    thread_id = user_input.thread_id or str(uuid4())
    user_id = user_input.user_id or str(uuid4())

    configurable = {
        "thread_id": thread_id,
        "user_id": user_id,
        "model": user_input.model
    }

    config = RunnableConfig(
        configurable=configurable
    )

    input = {"messages": [HumanMessage(content=user_input.message)]}

    response_events = agent.ainvoke(input=input, config=config)

    return response_events


app.include_router(router)
