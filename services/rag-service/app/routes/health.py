from fastapi import APIRouter, Response
from qdrant_client import QdrantClient
import redis

from app.config import settings

router = APIRouter()


@router.get("/health")
def health(response: Response):
    checks = {}

    try:
        QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port).get_collections()
        checks["qdrant"] = "ok"
    except Exception:
        checks["qdrant"] = "down"

    try:
        redis.Redis(host=settings.redis_host, port=settings.redis_port).ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "down"

    healthy = all(v == "ok" for v in checks.values())
    if not healthy:
        response.status_code = 503

    return {
        "status": "ok" if healthy else "degraded",
        "service": "intellix-rag-service",
        "checks": checks,
    }