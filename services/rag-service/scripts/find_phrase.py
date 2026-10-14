"""Search the evaluation corpus for a word or phrase, to help pick gold phrases.

Place in services/rag-service/scripts/ and run from services/rag-service:

    python -m scripts.find_phrase "sick days"
    python -m scripts.find_phrase NumericDate

For every document it prints how many times the phrase appears and a short
snippet (with the page number for PDFs). A good gold phrase for a question
appears exactly ONCE in the whole corpus.
"""
import re
import sys
from pathlib import Path

from app.services.parser import SUPPORTED, parse_file

CORPUS = Path(__file__).resolve().parents[3] / "evaluation" / "datasets" / "corpus"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.find_phrase "some phrase"')
        return 1

    term = norm(" ".join(sys.argv[1:])).lower()
    total = 0

    for path in sorted(CORPUS.iterdir()):
        if path.suffix.lower() not in SUPPORTED:
            continue
        doc_hits = 0
        snippets: list[str] = []
        for section in parse_file(path):
            text = norm(section.text)
            low = text.lower()
            count = low.count(term)
            if not count:
                continue
            doc_hits += count
            if len(snippets) < 2:
                i = low.find(term)
                lo, hi = max(0, i - 90), min(len(text), i + len(term) + 90)
                where = f"p{section.page}" if section.page else "-"
                snippets.append(f"   [{where}] ...{text[lo:hi]}...")
        if doc_hits:
            total += doc_hits
            print(f"{path.name}: {doc_hits} hit(s)")
            print("\n".join(snippets))

    print(f"\nTotal hits across corpus: {total}")
    if total == 1:
        print("Unique phrase: good gold candidate.")
    elif total == 0:
        print("Not found. Check spelling, or hyphenation/line breaks in the PDF.")
    else:
        print("Appears more than once: lengthen the phrase until it is unique.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
