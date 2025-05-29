from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .services import (
    test_openai_service,
    test_supabase_service,
    process_movie_data,
    find_recommendations,
)

router = APIRouter(prefix="/api", tags=["movies"])

# ---------- Pydantic models ----------
class MovieIn(BaseModel):
    content: str = Field(..., description="Plot or chunk text to embed")

class QueryIn(BaseModel):
    q1: str
    q2: str
    q3: str

class MovieOut(BaseModel):
    id: int
    content: str
    similarity: float

# ---------- Test endpoints ----------
@router.get("/test-openai", summary="Ping OpenAI embeddings")
async def test_openai_endpoint():
    try:
        return await test_openai_service()
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.get("/test-supabase", summary="Ping Supabase vector search")
async def test_supabase_endpoint():
    try:
        return await test_supabase_service()
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# ---------- Main endpoints ----------
@router.post(
    "/embed",
    summary="Embed and store a movie chunk",
    response_model=dict,      # o MovieOut si guardas y devuelves
)
async def embed_movie_data_endpoint(item: MovieIn):
    try:
        return await process_movie_data(item.dict())
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post(
    "/recommend",
    summary="Return best-matching movie",
    response_model=MovieOut,
)
async def get_recommendations_endpoint(query: QueryIn) -> MovieOut:
    try:
        return await find_recommendations(query.dict())
    except Exception as e:
        raise HTTPException(500, detail=str(e))