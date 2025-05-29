from openai import AsyncOpenAI
import os
client = AsyncOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])

async def chat_summarize(text: str) -> str:
    messages = [
        {"role": "system", "content": "Resume en una frase qué busca el usuario"},
        {"role": "user", "content": text},
    ]
    resp = await client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0.3
    )
    return resp.choices[0].message.content.strip()

async def get_embedding(text: str) -> list[float]:
    resp = await client.embeddings.create(
        model="text-embedding-ada-002", input=text
    )
    return resp.data[0].embedding
