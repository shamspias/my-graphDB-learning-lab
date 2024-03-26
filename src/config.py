from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str = "neo4j"
    DIFFBOT_API_KEY: str = "6c"
    LLM_API_KEY: str
    LLM_NAME: str = "groq"
    LLM_API_ENDPOINT: str = "https://api.example.com"
    REDIS_URL: str = "redis://localhost:6379/5"
    SYSTEM_INSTRUCTION: str = "Guide on integrating Neo4j with LLM."

    # Observatory by Langsmith
    LANGCHAIN_TRACING_V2: Optional[str] = Field(default=True)
    LANGCHAIN_ENDPOINT: Optional[str] = Field(default="https://api.smith.langchain.com")
    LANGCHAIN_API_KEY: Optional[str] = Field(default=None)
    LANGCHAIN_PROJECT: Optional[str] = Field(default=None)

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
