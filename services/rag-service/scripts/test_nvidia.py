from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.nvidia_api_key, base_url=settings.nvidia_base_url)

# Test 1: chat
chat = client.chat.completions.create(
    model=settings.llm_model,
    messages=[{"role": "user", "content": "Say hello in five words."}],
    max_tokens=1000,
)
choice = chat.choices[0]
print("finish_reason:", choice.finish_reason)
print("content:", choice.message.content)
print("raw message:", choice.message.model_dump())

# Test 2: embeddings
q = client.embeddings.create(
    model=settings.embedding_model,
    input=["How many remote days are allowed?"],
    encoding_format="float",
    extra_body={"input_type": "query", "truncate": "END"},
)
print("Query dimension:", len(q.data[0].embedding))