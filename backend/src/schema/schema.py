from pydantic import BaseModel, Field, SerializeAsAny

from backend.src.schema.models import AllModelEnum, OpenAIModelName, FakeModelName


class UserInput(BaseModel):
    message: str = Field(
        description="Input to the agent provided by the user",
        examples=["What is the weather like today?", "Tell me a joke about cats."],
    )
    model: SerializeAsAny[AllModelEnum] | None = Field(
        description="The model to use for the agent",
        default=OpenAIModelName.GPT_4O_MINI,
        examples=[OpenAIModelName.GPT_4O_MINI, FakeModelName.FAKE],
    )
    thread_id: str | None = Field(
        description="Unique identifier for the conversation thread",
        default=None,
        examples=["thread123", "thread456"],
    )
    user_id: str | None = Field(
        description="Unique identifier for the user",
        default=None,
        examples=["user123", "user456"],
    )
