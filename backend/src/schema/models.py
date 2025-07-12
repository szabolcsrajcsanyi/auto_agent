from enum import StrEnum
from typing import TypeAlias


class OpenAIModelName(StrEnum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"


class FakeModelName(StrEnum):
    FAKE = "fake"


AllModelEnum: TypeAlias = (
    OpenAIModelName 
    | FakeModelName
)
