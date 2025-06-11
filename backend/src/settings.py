from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    SecretStr
)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(

    )
    OPENAI_API_KEY: SecretStr
    TAVILY_API_KEY: SecretStr