import uuid

from app.services.parser import parse_file
from app.services.chunker import chunk_sections
from app.services.embeddings import embed_passages, embed_query
from app.services.vectorstore import upsert_chunks, search

path = "scripts/sample_policy.txt"
chunks = chunk_sections(parse_file(path), chunk_size=200, overlap=40)
print(f"Chunks: {len(chunks)}")

vectors = embed_passages([c.text for c in chunks])
print(f"Vectors: {len(vectors)} x {len(vectors[0])}")

n = upsert_chunks(chunks, vectors, document_id=str(uuid.uuid4()), filename="sample_policy.txt")
print(f"Stored: {n} points")

for question in [
    "How many days can I work from home?",
    "How much paid leave do employees get?",
    "When do I need approval for travel costs?",
]:
    hits = search(embed_query(question), limit=2)
    print(f"\nQ: {question}")
    for h in hits:
        print(f"  score={h.score:.3f} | {h.payload['text'][:80]!r}")