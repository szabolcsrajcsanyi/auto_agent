from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=load_dotenv(),
        env_file_encoding='utf-8',
    )
    OPENAI_API_KEY: SecretStr
    TAVILY_API_KEY: SecretStr

    MODE: str | None = None

    def is_dev(self) -> bool:
        return self.MODE == "dev"