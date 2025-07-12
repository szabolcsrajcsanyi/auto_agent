from functools import cache
from typing import TypeAlias
from langchain_community.chat_models import FakeListChatModel
from langchain_openai import ChatOpenAI

from schema.models import (
    AllModelEnum,
    OpenAIModelName,
    FakeModelName
)


_MODEL_TABLE = (
    {m: m.value for m in OpenAIModelName}
    | {m: m.value for m in FakeModelName}
)


class FakeToolModel(FakeListChatModel):
    def __init__(self, responses: list[str]):
        super().__init__(responses=responses)

    def bind_tools(self, tools):
        return self


MODELT: TypeAlias = (
    ChatOpenAI
    | FakeListChatModel
)


@cache
def get_model(model_name: AllModelEnum) -> MODELT:
    api_model_name = _MODEL_TABLE.get(model_name)
    if not api_model_name:
        raise ValueError(f"Model {model_name} is not supported.")
    
    if api_model_name in OpenAIModelName:
        return ChatOpenAI(model=api_model_name, temperature=0.5, streaming=True)
  
    if api_model_name in FakeModelName:
        return FakeToolModel(responses=["This is a test response from the fake model."])
    
    raise ValueError(f"Unsupported model: {model_name}")
