# app/vector_db.py
from typing import List, TypedDict, Any
import os
from supabase import create_client, Client
import asyncio

# ---------- Types ----------
class MovieMatch(TypedDict):
    id:        int
    content:   str
    similarity: float  # 0–1 (1 = identical)

# ---------- Supabase client ----------
sb: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_API_KEY"],
)

# ---------- Search helper ----------
async def search_similar_movies(
    embedding: List[float],
    *,
    top_k: int = 4,
    threshold: float = 0.5,
) -> List[MovieMatch]:
    """
    Calls the SQL function match_movies (see schema below) and returns
    a list sorted by similarity DESC.

    SQL reference in Supabase:
    ----------------------------------------------------------
    create or replace function match_movies (
        query_embedding vector(1536),
        match_threshold float,
        match_count int
    ) returns table (
        id bigint,
        content text,
        similarity float
    ) ...
    ----------------------------------------------------------
    """
    # Important: supabase-py is *sync*; run it in a thread so it won't block
    loop = asyncio.get_running_loop()
    res = await loop.run_in_executor(
        None,
        lambda: sb.rpc(
            "match_movies",
            {
                "query_embedding": embedding,
                "match_threshold": threshold,
                "match_count": top_k,
            },
        ).execute(),
    )

    if getattr(res, "error", None):
        raise RuntimeError(f"Supabase RPC error: {res.error}")

    rows: List[MovieMatch] = res.data or []  # type: ignore[attr-defined]
    return rows