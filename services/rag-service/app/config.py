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
    nvidia_api_key: str = ""
    nvidia_base_url: str = "https://integrate.api.nvidia.com/v1"
    llm_model: str = "meta/llama-3.1-70b-instruct"
    embedding_model: str = "nvidia/nv-embedqa-e5-v5"


settings = Settings()