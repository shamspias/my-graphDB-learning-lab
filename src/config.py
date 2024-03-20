from pydantic import BaseSettings


class Settings(BaseSettings):
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str = "neo4j"
    LLM_API_KEY: str
    LLM_NAME: str = "groq"
    LLM_API_ENDPOINT: str = "https://api.example.com"
    REDIS_URL: str = "redis://localhost:6379/5"
    SYSTEM_INSTRUCTION: str = "Guide on integrating Neo4j with LLM."

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
