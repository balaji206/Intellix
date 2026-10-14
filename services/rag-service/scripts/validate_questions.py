"""Validate evaluation/datasets/questions.json against the corpus.

Place in services/rag-service/scripts/ and run from services/rag-service
(with the venv active):

    python -m scripts.validate_questions

Checks
- every question has a real question text (no TODO placeholders)
- type is one of exact, semantic, multi, cross, unanswerable
- unanswerable questions have doc/gold/answer = null
- every other question names an existing corpus file and a gold phrase
- each gold phrase is found in that file, exactly once in the file AND once in the
  whole corpus (so the label is unambiguous)
"""
import json
import re
from collections import Counter
from pathlib import Path

from app.services.parser import SUPPORTED, parse_file

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "evaluation" / "datasets"
CORPUS = DATA / "corpus"
TYPES = {"exact", "semantic", "multi", "cross", "unanswerable"}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def as_list(value):
    return value if isinstance(value, list) else [value]


def main() -> int:
    questions = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))

    texts: dict[str, str] = {}
    for path in sorted(CORPUS.iterdir()):
        if path.suffix.lower() in SUPPORTED:
            texts[path.name] = norm(" ".join(s.text for s in parse_file(path)))
    print(f"Corpus files loaded: {len(texts)}")

    problems = 0

    def problem(qid: str, message: str) -> None:
        nonlocal problems
        problems += 1
        print(f"[{qid}] {message}")

    seen_ids: set[str] = set()
    for q in questions:
        qid = q.get("id", "?")
        if qid in seen_ids:
            problem(qid, "duplicate id")
        seen_ids.add(qid)

        if q.get("type") not in TYPES:
            problem(qid, f"type must be one of {sorted(TYPES)}")
        text = (q.get("question") or "").strip()
        if not text or text.upper().startswith("TODO"):
            problem(qid, "question text is missing or still a TODO")

        if q.get("type") == "unanswerable":
            if q.get("doc") or q.get("gold") or q.get("answer"):
                problem(qid, "unanswerable question must have doc, gold and answer = null")
            continue

        docs, golds = as_list(q.get("doc")), as_list(q.get("gold"))
        if len(docs) != len(golds) or None in docs or None in golds:
            problem(qid, "doc and gold must be non-empty and the same length")
            continue
        if not (q.get("answer") or "").strip() or str(q["answer"]).upper().startswith("TODO"):
            problem(qid, "answer is missing or still a TODO")
        if q.get("type") == "cross" and len(docs) < 2:
            problem(qid, "cross question needs two docs and two gold phrases")

        for doc, gold in zip(docs, golds):
            if str(gold).upper().startswith("TODO"):
                problem(qid, "gold phrase is still a TODO")
                continue
            if doc not in texts:
                problem(qid, f"file not in corpus: {doc}")
                continue
            phrase = norm(gold)
            in_doc = texts[doc].count(phrase)
            in_corpus = sum(t.count(phrase) for t in texts.values())
            if in_doc == 0:
                problem(qid, f"gold phrase NOT found in {doc}: {gold!r}")
            elif in_doc > 1:
                problem(qid, f"gold phrase appears {in_doc}x in {doc} (lengthen it): {gold!r}")
            elif in_corpus > 1:
                problem(qid, f"gold phrase also appears in another file ({in_corpus} hits): {gold!r}")

    print(f"\nQuestions: {len(questions)}  by type: {dict(Counter(q.get('type') for q in questions))}")
    print("All labels valid." if problems == 0 else f"{problems} problem(s) to fix.")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())