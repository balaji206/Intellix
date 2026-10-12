import uuid
from pathlib import Path
from app.services.llm import chat
from app.services.chunker import chunk_sections
from app.services.embeddings import embed_passages, embed_query
from app.services.parser import parse_file
from app.services.vectorstore import search, upsert_chunks
from app.services.llm import chat

SYSTEM_PROMPT = (
    "You are Intellix, an assistant that answers questions using ONLY the numbered "
    "sources provided. Rules:\n"
    "1. Use only information in the sources. Do not use outside knowledge.\n"
    "2. After each claim, cite the supporting source like [1] or [2].\n"
    "3. If the sources do not contain the answer, reply exactly: "
    "\"I couldn't find this in the provided documents.\"\n"
    "4. Be concise."
)

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

    SYSTEM_PROMPT = (
    "You are Intellix, an assistant that answers questions using ONLY the numbered "
    "sources provided. Rules:\n"
    "1. Use only information in the sources. Do not use outside knowledge.\n"
    "2. After each claim, cite the supporting source like [1] or [2].\n"
    "3. If the sources do not contain the answer, reply exactly: "
    "\"I couldn't find this in the provided documents.\"\n"
    "4. Be concise."
)


def answer(question: str, limit: int = 5) -> dict:
    sources = retrieve(question, limit=limit)

    context = "\n\n".join(
        f"[{i}] ({s['filename']}, page {s['page']})\n{s['text']}"
        for i, s in enumerate(sources, start=1)
    )
    user_prompt = f"Sources:\n{context}\n\nQuestion: {question}"

    text = chat(SYSTEM_PROMPT, user_prompt)

    return {
        "question": question,
        "answer": text,
        "sources": [
            {
                "ref": i,
                "filename": s["filename"],
                "page": s["page"],
                "score": s["score"],
                "text": s["text"],
            }
            for i, s in enumerate(sources, start=1)
        ],
    }