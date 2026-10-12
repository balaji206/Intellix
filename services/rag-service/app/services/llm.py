from functools import lru_cache

from openai import OpenAI

from app.config import settings


@lru_cache
def _get_client() -> OpenAI:
    return OpenAI(
        api_key=settings.nvidia_api_key or "missing",
        base_url=settings.nvidia_base_url,
        timeout=120,
    )


def chat(system: str, user: str, max_tokens: int = 2000) -> str:
    resp = _get_client().chat.completions.create(
        model=settings.llm_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.1,
    )
    return (resp.choices[0].message.content or "").strip()