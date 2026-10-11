from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.nvidia_api_key, base_url=settings.nvidia_base_url)

CHAT = [
    "google/gemma-3-12b-it",
    "google/gemma-4-31b-it",
    "google/gemma-3-4b-it",
    "mistralai/mistral-7b-instruct-v0.3",
    "mistralai/mistral-large-2-instruct",
    "nv-mistralai/mistral-nemo-12b-instruct",
    "ibm/granite-3.0-8b-instruct",
    "openai/gpt-oss-20b",
    "nvidia/llama-3.1-nemotron-51b-instruct",
    "nvidia/llama-3.1-nemotron-ultra-253b-v1",
]

EMBED = [
    "nvidia/llama-3.2-nv-embedqa-1b-v1",
    "nvidia/nv-embedqa-mistral-7b-v2",
    "nvidia/embed-qa-4",
    "nvidia/nemotron-3-embed-1b",
    "snowflake/arctic-embed-l",
]

print("== CHAT ==")
for m in CHAT:
    try:
        r = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "Say hello in five words."}],
            max_tokens=30,
            timeout=30,
        )
        print("OK  ", m, "->", (r.choices[0].message.content or "").strip()[:40])
    except Exception as e:
        print("FAIL", m, "->", str(e)[:70])

print("\n== EMBEDDINGS ==")
for m in EMBED:
    try:
        r = client.embeddings.create(
            model=m,
            input=["Remote work policy allows two days per week."],
            encoding_format="float",
            extra_body={"input_type": "passage", "truncate": "END"},
            timeout=30,
        )
        print("OK  ", m, "-> dim", len(r.data[0].embedding))
    except Exception as e:
        print("FAIL", m, "->", str(e)[:70])