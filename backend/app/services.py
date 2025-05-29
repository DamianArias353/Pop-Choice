# backend/app/services.py
# Keep only necessary imports for your API service functions
import json # Only needed if process_movie_data or find_recommendations uses json
import os # Needed for os.getenv calls (if still present or needed)

# Import functions from the low-level modules using ABSOLUTE IMPORTS relative to 'app'
# Keep imports needed for the API service functions
from app.embeddings import get_embedding # Needed for process_movie_data and find_recommendations
from app.vector_db import save_movie_with_embedding 
from openai import AsyncOpenAI  # Needed for process_movie_data
# REMOVE THIS LINE: from app.data.movies import MOVIES_DATA # No longer needed

# REMOVE THESE IMPORTS IF ONLY USED BY SEEDING LOGIC:
# import asyncio # Check if any service function uses asyncio directly
# from pathlib import Path # Only needed for file reading
# from langchain.text_splitter import RecursiveCharacterTextSplitter # Only needed for splitting

# Check if get_movies is still used in a test service endpoint, if so, import it
# from app.vector_db import get_movies
openai_client = AsyncOpenAI()                        # lee OPENAI_API_KEY desde env

SYSTEM_PROMPT = (
    "You are an enthusiastic movie expert who loves recommending movies to people. "
    "Answer briefly using the provided context. If unsure, say you don't know."
)

# --- Service functions corresponding to test endpoints (Keep these) ---
async def test_openai_service():
    """
    Service logic to test OpenAI embedding function.
    Calls get_embedding from app.embeddings.
    """
    test_text = "Hello from the FastAPI backend service!"
    # Assume get_embedding might be async and await it
    embedding = get_embedding(test_text) # Await if get_embedding is async

    if embedding is None:
        raise ValueError("Failed to get embedding from OpenAI in service.")

    return {"message": "OpenAI embedding successful from service", "embedding_start": embedding[:5]}

async def test_supabase_service():
     """
     Service logic to test Supabase connection and data fetch function.
     Calls get_movies from app.vector_db (if get_movies exists and is relevant).
     """
     # Assuming get_movies is still needed for this test endpoint
     # from app.vector_db import get_movies # Import if needed
     # movies_data = get_movies(limit=2) # Await if get_movies is async

     # You might need to create a simple test function in vector_db.py
     # that just checks if the client is initialized and can connect.
     # Or, since the seed script populated the table, test fetching actual data.

     # Example using a function from vector_db to check connection/fetch data
     from app.vector_db import get_movies # Assuming get_movies still exists and works
     movies_data = get_movies(limit=2) # Await if async

     if movies_data is None or not hasattr(movies_data, 'data'):
         # You might check for specific error messages here if vector_db provides them
          raise ValueError("Failed to fetch data from Supabase in service.")

     return {"message": "Supabase connection successful from service", "data": movies_data.data}


# --- Service functions for your main logic (Keep these) ---

# This function will be called by the /embed API endpoint
async def process_movie_data(item: dict): # Replace dict with a proper Pydantic model later
    """
    Business logic to process single movie data, get embedding, and save to DB.
    This is for adding NEW movies via the API.
    Assumes item is a dictionary with 'content' and other movie fields.
    Saves one embedding per movie.
    """
    print("Processing single movie data in service...")
    # Extract text for embedding - adjust keys based on the input item structure
    text_to_embed = item.get("content", "") # Assuming the input item has a 'content' field

    if not text_to_embed:
        raise ValueError("Movie item missing 'content' field for embedding.")

    # Get embedding for the content (await if get_embedding becomes async)
    embedding = get_embedding(text_to_embed)

    if embedding is None:
         raise ValueError("Could not generate embedding for movie data.")

    # Save the movie data and its embedding using the vector_db function (MUST be async)
    # This function needs to save a SINGLE movie object and its embedding
    saved = await save_movie_with_embedding(item, embedding) # Ensure save_movie_with_embedding is async

    if not saved:
        raise RuntimeError(f"Failed to save movie '{item.get('title', 'Unknown')}' to database.")

    return {"status": "Movie processed and saved successfully", "title": item.get('title')}


# -----------------------------------------------------------------------------
async def find_recommendations(query: dict):
    """
    1) Embedding del input
    2) Búsqueda de chunks en Supabase/pgvector
    3) Prompt + ChatCompletion
    """
    print("Finding recommendations in service...")

    user_input = query.get("user_input")
    if not user_input:
        raise ValueError("User query missing 'user_input' field.")

    # 1) Embedding de la consulta
    query_embedding = await get_embedding(user_input)   # si get_embedding es async
    # query_embedding = get_embedding(user_input)       # si es sync

    # 2) Buscar en la base vectorial (chunks ya embebidos)
    # Esta función debe devolver algo como:
    #   [{"content": "...", "similarity": 0.87}, ...]
    matches = await search_similar_movies(
        embedding=query_embedding,
        threshold=0.50,
        n_results=4
    )

    if not matches:
        return {"answer": "Sorry, I don't have enough data to answer that."}

    context = "\n".join(m["content"] for m in matches)

    # 3) ChatCompletion
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",
         "content": f"Context: {context}\nQuestion: {user_input}"}
    ]

    resp = await openai_client.chat.completions.create(
        model="gpt-4o-mini",          # o el modelo que uses
        messages=messages,
        temperature=0.65,
        frequency_penalty=0.5,
    )

    answer = resp.choices[0].message.content
    return {"answer": answer}
