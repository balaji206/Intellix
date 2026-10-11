from functools import lru_cache

from openai import OpenAI

from app.config import settings

BATCH_SIZE = 16


@lru_cache
def _get_client() -> OpenAI:
    return OpenAI(
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_base_url,
        timeout=60,
    )

BATCH_SIZE = 16


def _embed(texts: list[str], input_type: str) -> list[list[float]]:
    vectors: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        resp = _client.embeddings.create(
            model=settings.embedding_model,
            input=batch,
            encoding_format="float",
            extra_body={"input_type": input_type, "truncate": "END"},
        )
        vectors.extend(item.embedding for item in resp.data)
    return vectors


def embed_passages(texts: list[str]) -> list[list[float]]:
    """For document chunks."""
    return _embed(texts, "passage")


def embed_query(text: str) -> list[float]:
    """For a user's question."""
    return _embed([text], "query")[0]