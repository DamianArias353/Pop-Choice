# embeddings_runner.py
import os
import asyncio
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from supabase import create_client, Client
from openai import AsyncOpenAI   # official async client (>=1.3.0)

# ───────────────────────── 1. CONFIG  ──────────────────────────
# Set these four env-vars once (e.g. in Docker secrets / .env)
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
SUPABASE_URL        = os.getenv("SUPABASE_URL")            # e.g. "https://xxx.supabase.co"
SUPABASE_API_KEY= os.getenv("SUPABASE_API_KEY")    # API-role key (rw on the table)
SUPABASE_TABLE      = "movies"                             # destination table name

# Create clients
openai = AsyncOpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# ──────────────────────── 2. TEXT SPLITTING  ───────────────────
def split_document(path: str):
    """Return a list[Document] produced by LangChain."""
    text = Path(path).read_text(encoding="utf-8")
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=35)
    return splitter.create_documents([text])

# ───────────────────── 3. EMBEDDING + UPSERT  ──────────────────
async def create_and_store_embeddings(path: str | None = None):
    # Resolve default data path when none is provided.
    if path is None:
        base_dir = Path(__file__).resolve().parent  # /app in container, project root locally
        candidate = base_dir / "data" / "movies.txt"
        if not candidate.exists():                  # fallback for local execution
            candidate = base_dir / "app" / "data" / "movies.txt"
        path = str(candidate)
    docs = split_document(path)

    # Batch-process each chunk → embedding
    async def embed(doc):
        resp = await openai.embeddings.create(
            model="text-embedding-ada-002",
            input=doc.page_content
        )
        return {
            "content":  doc.page_content,
            "embedding": resp.data[0].embedding   # list[float]
        }

    records = await asyncio.gather(*(embed(d) for d in docs))

    # Supabase-py returns an APIResponse object (not a dict), so use its attributes:
    res = supabase.table(SUPABASE_TABLE).insert(records).execute()

    # Handle error first
    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase insert failed: {res.error}")

    # HTTP status check (falls back to 200 when attribute not present)
    status = getattr(res, "status_code", 200)
    if status not in (200, 201):
        body = res.json() if hasattr(res, "json") else repr(res)
        raise RuntimeError(f"Supabase insert failed (HTTP {status}): {body}")

    print("SUCCESS ✓  Stored", len(records), "embeddings in Supabase")

# ──────────────────────────── 4. MAIN  ─────────────────────────
if __name__ == "__main__":
    asyncio.run(create_and_store_embeddings())