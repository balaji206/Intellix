# Phase 1 Results

Setup: fixed-size chunking (800 chars, 150 overlap), embeddings nvidia/nemotron-3-embed-1b, LLM openai/gpt-oss-20b, top-k = 5.
Documents: sample_policy.txt (1 chunk), test.pdf (3 chunks).

| # | Type | Question | Answer | Cited | Top score / gap | Time (s) | Correct? | Citation OK? |
|---|---|---|---|---|---|---|---|---|
| 1 | Direct | How much paid leave do employees get? | Employees receive 20 days of paid leave per year. [1] | [1] sample_policy.txt | 0.381 / 0.385 | 5.9 | Yes | Yes |
| 2 | Direct | How many days of unused leave can be carried over? | Unused leave can be carried over for a maximum of 5 days. [1] | [1] sample_policy.txt | 0.449 / 0.463 | 2.2 | Yes | Yes |
| 3 | Direct | What is required for remote work besides manager approval? | Remote work also requires a stable internet connection and the use of the company VPN. [1] | [1] sample_policy.txt | 0.466 / 0.455 | 9.3 | Yes | Yes |
| 4 | Direct | Which issue number does the solution proposal address? | The solution proposal addresses issue **#27908**【1】【2】【3】 | - | 0.324 / 0.205 | 3.1 | Yes | No-Format Broken |
| 5 | Reworded | Can I work from my house some days? | Yes. Employees may work remotely up to two days per week, but you need manager approval for those days. [1] | [1] sample_policy.txt | 0.336 / 0.337 | 6.5 | Yes | Yes |
| 6 | Reworded | How many vacation days do full-timers get each year? | Full‑time employees receive 20 days of paid leave per year. [1] | [1] sample_policy.txt | 0.310 / 0.323 | 3.7 | Yes | Yes |
| 7 | Reworded | What is wrong with reordering items on an iPhone? | Reordering items on an iPhone (or iPad) fails because the drag‑and‑drop interaction does not work in iOS Safari/Chrome. The underlying SortableJS dependency lacks pointer‑event support for iOS Safari, so the drag‑handle cannot be used to reorder collection rec | [1] test.pdf p1, [2] test.pdf p1, [3] test.pdf p1 | 0.525 / 0.127 | 6.7 | Partly |Coarse (cites all three chunks, all page 1, so it can’t tell you which one supports which claim) |
| 8 | Not in docs | What is the company stock price? | I couldn't find this in the provided documents. | - | 0.062 / 0.071 | 2.5 |Yes | n/a |
| 9 | Not in docs | What is the leave policy for contractors? | I couldn't find this in the provided documents. | - | 0.314 / 0.273 | 2.1 | Yes | n/a |
| 10 | Multi-topic | What is the leave carry-over limit and the travel approval rule? | The leave carry‑over limit is **5 days** [1].   Travel expenses exceeding **5000 INR** require prior approval from the department head [1]. | [1] sample_policy.txt | 0.526 / 0.529 | 10.2 |  Yes | Yes, but Coarse (single chunk) |


## Observations
- Worked: grounded answers on 10/10 questions (Q7 pending manual check), correct "not found"
  on 2/2 unanswerable questions, semantic matching on reworded questions (Q5, Q6),
  page numbers for the PDF.
- Weak: citation format drift (Q4 used 【1】【2】【3】 instead of [1]); the policy file is a single
  chunk, so citations are coarse; multi-fact answers cite one source for everything.
- Score finding: Q9 (unanswerable, top score 0.314) scored above Q6 (answerable, 0.310), so a
  fixed similarity threshold cannot separate answerable from unanswerable questions.
  Answer validation has to look at the text.
- Limitation: only 4 chunks indexed with top-k = 5, so every chunk was retrieved on every
  question. Retrieval quality was not really tested. Phase 2 needs a larger corpus.
- Latency: 2.1 to 10.2 s per question, mean 5.2 s (one run of 10 questions). Refusals were
  fastest (about 2 s) because the output is short.