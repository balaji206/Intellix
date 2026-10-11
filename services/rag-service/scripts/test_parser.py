import sys
from app.services.parser import parse_file

path = sys.argv[1] if len(sys.argv) > 1 else "scripts/sample_policy.txt"
sections = parse_file(path)

print(f"Sections: {len(sections)}")
for s in sections:
    print(f"--- page={s.page} | {len(s.text)} chars ---")
    print(s.text[:300])