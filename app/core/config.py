from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise AI Knowledge Copilot"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "bge-m3"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()