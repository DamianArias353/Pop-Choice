from fastapi import APIRouter, HTTPException # Use APIRouter here
# Import functions from the service layer
from .services import (
    test_openai_service, # Function you'd define in services.py
    test_supabase_service, # Function you'd define in services.py
    process_movie_data, # Function for the /embed logic
    find_recommendations # Function for the /recommend logic
)

router = APIRouter() # Create an API router instance

@router.get("/test-openai")
async def test_openai_endpoint():
    """
    API endpoint to test the OpenAI embedding function (calls service).
    """
    print("Received request to /test-openai")
    try:
        result = await test_openai_service() # Call the service function
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) # Handle service errors


@router.get("/test-supabase")
async def test_supabase_endpoint():
    """
    API endpoint to test the Supabase connection (calls service).
    """
    print("Received request to /test-supabase")
    try:
         result = await test_supabase_service() # Call the service function
         return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e)) # Handle service errors

# --- Your Main Endpoints (Using Pydantic models for input later) ---

@router.post("/embed")
async def embed_movie_data_endpoint(item: dict): # Replace dict with Pydantic model
    """
    Endpoint to receive data, process, and store (calls service).
    """
    print("Received request to /embed")
    try:
        result = await process_movie_data(item) # Call the service function
        return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e)) # Handle service errors

@router.post("/recommend")
async def get_recommendations_endpoint(query: dict): # Replace dict with Pydantic model
    """
    Endpoint to receive query, find recommendations (calls service).
    """
    print("Received request to /recommend")
    try:
        result = await find_recommendations(query) # Call the service function
        return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e)) # Handle service errors
