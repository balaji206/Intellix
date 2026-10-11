from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.nvidia_api_key, base_url=settings.nvidia_base_url)

for m in sorted(client.models.list().data, key=lambda x: x.id):
    print(m.id)