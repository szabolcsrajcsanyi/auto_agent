from pydantic import BaseModel, Field


class UserInput(BaseModel):
    message: str = Field(
        description="Input to the agent provided by the user",
        examples=["What is the weather like today?", "Tell me a joke about cats."],
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
