"""Print random passages from a corpus document, to help you write questions.

Place in services/rag-service/scripts/ and run from services/rag-service
(with the venv active):

    python -m scripts.sample_passages rfc7519            # 5 passages from rfc7519-jwt.txt
    python -m scripts.sample_passages NIST --n 8
    python -m scripts.sample_passages gitlab-time --n 3 --seed 1

Options
    --n N       number of passages (default 5)
    --len N     passage length in characters (default 450)
    --seed N    fix the random choice so you get the same passages again

The first argument is any part of a file name. Run it with no arguments to
list the corpus files.
"""
import random
import re
import sys
from pathlib import Path

from app.services.parser import SUPPORTED, parse_file

CORPUS = Path(__file__).resolve().parents[3] / "evaluation" / "datasets" / "corpus"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    files = [p for p in sorted(CORPUS.iterdir()) if p.suffix.lower() in SUPPORTED]
    args = sys.argv[1:]
    n, length, seed, name = 5, 450, None, None

    i = 0
    while i < len(args):
        if args[i] == "--n":
            n, i = int(args[i + 1]), i + 2
        elif args[i] == "--len":
            length, i = int(args[i + 1]), i + 2
        elif args[i] == "--seed":
            seed, i = int(args[i + 1]), i + 2
        else:
            name, i = args[i], i + 1

    if not name:
        print("Corpus files:")
        for p in files:
            print("  ", p.name)
        print("\nUsage: python -m scripts.sample_passages <part of file name> [--n 5] [--len 450] [--seed 1]")
        return 1

    matches = [p for p in files if name.lower() in p.name.lower()]
    if len(matches) != 1:
        print(f"{len(matches)} files match {name!r}: {[p.name for p in matches]}")
        return 1

    path = matches[0]
    sections = [(s.page, norm(s.text)) for s in parse_file(path) if norm(s.text)]
    if not sections:
        print("No text extracted from this file.")
        return 1

    rng = random.Random(seed)
    weights = [len(t) for _, t in sections]
    print(f"{path.name}: {len(sections)} section(s)\n")

    for k in range(1, n + 1):
        page, text = rng.choices(sections, weights=weights)[0]
        if len(text) <= length:
            passage = text
        else:
            start = rng.randint(0, len(text) - length)
            dot = text.find(". ", start)  # begin at a sentence start when possible
            if dot != -1 and dot + 2 < len(text) - length // 2:
                start = dot + 2
            passage = text[start : start + length]
        where = f"page {page}" if page else "no page"
        print(f"--- {k} ({where}) ---\n{passage}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())