# backend/app/services.py
# Keep only necessary imports for your API service functions
import json # Only needed if process_movie_data or find_recommendations uses json
import os # Needed for os.getenv calls (if still present or needed)

# Import functions from the low-level modules using ABSOLUTE IMPORTS relative to 'app'
# Keep imports needed for the API service functions
from app.embeddings import get_embedding, chat_summarize # Added chat_summarize
from app.vector_db import search_similar_movies
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
    embedding = await get_embedding(test_text) # Await if get_embedding is async

    if embedding is None:
        raise ValueError("Failed to get embedding from OpenAI in service.")

    return {"message": "OpenAI embedding successful from service", "embedding_start": embedding[:5]}

async def test_supabase_service():
     """
     Service logic to test Supabase connection and data fetch function.
     Calls get_movies from app.vector_db (if get_movies exists and is relevant).
     """
     # Quick connectivity test: fetch 1 movie id via RPC
     test_rows = await search_similar_movies([0.0]*1536, top_k=1, threshold=0.0)

     if test_rows is None:
         raise ValueError("Failed to fetch data from Supabase in service.")

     return {"message": "Supabase connection successful from service", "data": test_rows}


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
    embedding = await get_embedding(text_to_embed)

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
    1) Summarize user input using chat_summarize
    2) Get embedding of the summary
    3) Search for similar movie *chunks*
    4) Use top chunks as context for language model to generate a movie description
    5) Return the generated description and the similarity of the best chunk
    """
    print("Finding recommendations in service...")

    # Get the three questions
    q1 = query.get("q1", "")
    q2 = query.get("q2", "")
    q3 = query.get("q3", "")

    if not all([q1, q2, q3]):
        raise ValueError("Missing required questions in query.")

    # Combine questions for initial summarization
    combined_input = f"Favorite movie and why: {q1}\nMood for new or classic: {q2}\nFun or serious: {q3}"

    # Get a summary of what the user is looking for
    summary = await chat_summarize(combined_input)
    print(f"Summarized input: {summary}")

    # Get embedding of the summary for vector search
    query_embedding = await get_embedding(summary)

    # Search for similar movie chunks in the vector database
    matches = await search_similar_movies(
        embedding=query_embedding,
        threshold=0.50, # Adjust threshold as needed
        top_k=4         # Retrieve top 4 chunks
    )

    if not matches:
        # If no matches found, return a specific message
        return {"content": "Sorry, I couldn't find any movies matching your criteria.", "similarity": 0.0}

    # Format the top matching chunks as context for the language model
    # We'll use the 'content' of each matching chunk
    context = "\n---\n".join([m["content"] for m in matches])
    print(f"Context for LLM:\n{context}")

    # Use the language model (OpenAI Chat Completion) to generate a description
    # based on the context and the original user query
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\nBased on the following movie information chunks and the user's query, provide a concise description of the *most relevant* movie, highlighting why it matches the user's preferences. Include the movie title, year, and key plot points or characteristics mentioned in the context. Focus on the single best recommendation."},
        {"role": "user",
         "content": f"Movie Information Chunks:\n{context}\n\nUser Query: {summary}"}
    ]

    try:
        resp = await openai_client.chat.completions.create(
            model="gpt-4o-mini",  # or the model you prefer
            messages=messages,
            temperature=0.7,      # Adjust temperature for creativity vs. accuracy
            max_tokens=200,       # Limit the length of the description
        )
        generated_description = resp.choices[0].message.content.strip()
        print(f"Generated Description: {generated_description}")

        # Return the generated description and the similarity of the best match
        # We return the similarity of the best match as an indicator of confidence
        return {
            "content": generated_description,
            "similarity": matches[0]["similarity"]
        }

    except Exception as e:
        print(f"Error generating description with LLM: {e}")
        # Fallback in case of LLM error - maybe just return the top chunk content?
        # Or a generic error message
        return {"content": "Could not generate a detailed recommendation at this time.", "similarity": 0.0}
