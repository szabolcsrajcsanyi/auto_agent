from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    EMBEDDING_MODEL: str
    CHROMA_HOST: str
    CHROMA_PORT: int
    CHROMA_COLLECTION_NAME: str
