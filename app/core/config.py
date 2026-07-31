from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise AI Knowledge Copilot"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "bge-m3"
    llm_model: str = "qwen3:8b"
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_name: str = "enterprise_knowledge"
    jwt_secret_key: str = "change-me-in-production-please"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    database_url: str = "postgresql+asyncpg://localhost:5432/copilot"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()