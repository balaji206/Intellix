import re
import time
from pathlib import Path

import httpx

URL = "http://localhost:4000/ask"
OUT = Path(__file__).resolve().parents[3] / "docs" / "phase1-results.md"

QUESTIONS = [
    ("Direct", "How much paid leave do employees get?"),
    ("Direct", "How many days of unused leave can be carried over?"),
    ("Direct", "What is required for remote work besides manager approval?"),
    ("Direct", "Which issue number does the solution proposal address?"),
    ("Reworded", "Can I work from my house some days?"),
    ("Reworded", "How many vacation days do full-timers get each year?"),
    ("Reworded", "What is wrong with reordering items on an iPhone?"),
    ("Not in docs", "What is the company stock price?"),
    ("Not in docs", "What is the leave policy for contractors?"),
    ("Multi-topic", "What is the leave carry-over limit and the travel approval rule?"),
]


def clean(text: str, n: int = 260) -> str:
    return text.replace("\n", " ").replace("|", "/")[:n]


rows = []
with httpx.Client(timeout=180) as client:
    for i, (kind, q) in enumerate(QUESTIONS, 1):
        start = time.time()
        try:
            data = client.post(URL, json={"question": q, "limit": 5}).json()
        except Exception as e:
            rows.append(f"| {i} | {kind} | {q} | ERROR {e} | - | - | - | | |")
            continue
        secs = time.time() - start

        answer = data.get("answer", str(data))
        srcs = {s["ref"]: s for s in data.get("sources", [])}
        cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", answer)})
        cited_txt = ", ".join(
            f"[{n}] {srcs[n]['filename']}" + (f" p{srcs[n]['page']}" if srcs[n]["page"] else "")
            if n in srcs else f"[{n}] MISSING"
            for n in cited
        ) or "-"
        scores = [srcs[k]["score"] for k in sorted(srcs)]
        top = f"{scores[0]:.3f}" if scores else "-"
        gap = f"{scores[0] - scores[1]:.3f}" if len(scores) > 1 else "-"

        rows.append(
            f"| {i} | {kind} | {q} | {clean(answer)} | {cited_txt} | {top} / {gap} | {secs:.1f} | | |"
        )
        print(f"{i}. [{secs:.1f}s] {q}\n   {clean(answer, 160)}\n   cited: {cited_txt}\n")

header = (
    "# Phase 1 Results\n\n"
    "Setup: fixed-size chunking (800 chars, 150 overlap), embeddings nvidia/nemotron-3-embed-1b, "
    "LLM openai/gpt-oss-20b, top-k = 5.\n"
    "Documents: sample_policy.txt (1 chunk), test.pdf (3 chunks).\n\n"
    "| # | Type | Question | Answer | Cited | Top score / gap | Time (s) | Correct? | Citation OK? |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
print(f"Saved to {OUT}")