import sys
from app.services.parser import parse_file
from app.services.chunker import chunk_sections

path = sys.argv[1] if len(sys.argv) > 1 else "scripts/sample_policy.txt"
size = int(sys.argv[2]) if len(sys.argv) > 2 else 800
overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 150

chunks = chunk_sections(parse_file(path), chunk_size=size, overlap=overlap)

print(f"Chunks: {len(chunks)}")
for c in chunks:
    print(f"\n--- chunk {c.chunk_index} | page={c.page} | {len(c.text)} chars ---")
    print(c.text)