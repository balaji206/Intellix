from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# project root: services/rag-service/app/config.py -> 3 levels up
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_ENV, extra="ignore")

    rag_port: int = 8000
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    redis_host: str = "localhost"
    redis_port: int = 6379


settings = Settings()