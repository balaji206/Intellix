import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.config import settings
from app.services.chunker import Chunk

_client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    check_compatibility=False,
)


def ensure_collection() -> None:
    existing = [c.name for c in _client.get_collections().collections]
    if settings.qdrant_collection not in existing:
        _client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE,
            ),
        )


def upsert_chunks(
    chunks: list[Chunk],
    vectors: list[list[float]],
    document_id: str,
    filename: str,
) -> int:
    ensure_collection()
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload={
                "document_id": document_id,
                "filename": filename,
                "chunk_index": c.chunk_index,
                "page": c.page,
                "text": c.text,
            },
        )
        for c, vec in zip(chunks, vectors)
    ]
    _client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)


def search(query_vector: list[float], limit: int = 5):
    ensure_collection()
    return _client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=limit,
        with_payload=True,
    ).points