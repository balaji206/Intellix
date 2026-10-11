import uuid
from pathlib import Path

from app.services.chunker import chunk_sections
from app.services.embeddings import embed_passages, embed_query
from app.services.parser import parse_file
from app.services.vectorstore import search, upsert_chunks


def index_file(path: str | Path, filename: str, document_id: str | None = None) -> dict:
    document_id = document_id or str(uuid.uuid4())
    sections = parse_file(path)
    if not sections:
        raise ValueError("No extractable text found in the file")

    chunks = chunk_sections(sections)
    vectors = embed_passages([c.text for c in chunks])
    stored = upsert_chunks(chunks, vectors, document_id=document_id, filename=filename)
    return {"document_id": document_id, "filename": filename, "chunks": stored}


def retrieve(question: str, limit: int = 5) -> list[dict]:
    hits = search(embed_query(question), limit=limit)
    return [
        {
            "score": round(h.score, 4),
            "text": h.payload["text"],
            "filename": h.payload["filename"],
            "page": h.payload["page"],
            "document_id": h.payload["document_id"],
            "chunk_index": h.payload["chunk_index"],
        }
        for h in hits
    ]