import os
from supabase import create_client, Client


# Get Supabase credentials from environment variables
# Ensure SUPABASE_URL and SUPABASE_API_KEY are set in your .env
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_API_KEY")

# --- Add these print statements ---
print(f"DEBUG: Supabase URL found? {'Yes' if url else 'No'}")
print(f"DEBUG: Supabase Key found? {'Yes' if key else 'No'}")
if url:
    print(f"DEBUG: Supabase URL: {url}")
if key:
     print(f"DEBUG: Supabase Key starts with: {key[:5]}...") # Print first few chars


# Initialize Supabase client
# Check if credentials are available before creating the client
if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_API_KEY not found. Supabase client NOT initialized.")
    supabase: Client = None
else:
    try:
        # Ensure you are using the correct Supabase version and arguments for create_client
        supabase: Client = create_client(url, key)
        # print("Supabase client created successfully.") # Keep or remove debug prints
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        # This error happens if create_client call itself fails, not usually connection errors
        supabase: Client = None

# --- Placeholder/Example Function (Implement your actual DB logic here) ---

def get_movies(limit: int = 1):
    """
    Example function to fetch movies (replace with your actual table name).
    This is just for the initial test.
    You will add functions like save_movie_with_embedding and search_similar_movies here.
    """
    if supabase is None:
        print("Supabase client is None. Cannot fetch movies.")
        return None

    try:
        # --- REPLACE "your_movies_table" with your ACTUAL TABLE NAME ---
        table_name = "movies"
        # print(f"DEBUG: Attempting to fetch from Supabase table: {table_name}") # Keep or remove debug prints

        response = supabase.table(table_name).select("*").limit(limit).execute()

        if response and hasattr(response, 'data'):
             # print(f"DEBUG: Supabase query returned {len(response.data)} rows.") # Keep or remove debug prints
             return response
        else:
             # print("DEBUG: Supabase query returned empty or unexpected data.") # Keep or remove debug prints
             return None
    except Exception as e:
        print(f"Error fetching movies from Supabase: {e}")
        # This exception likely means the table doesn't exist or a connection issue during query
        return None

# --- Add Actual Database Interaction Functions Here ---

async def save_movie_with_embedding(movie_data: dict, embedding: list):
    """
    Saves a single movie's data and its embedding to the Supabase table.
    Uses upsert based on 'title' to avoid duplicates if run multiple times.
    """
    if supabase is None:
        print("Supabase client not initialized. Cannot save movie.")
        return None

    try:
        # --- REPLACE "your_movies_table" with your ACTUAL TABLE NAME ---
        table_name = "movies"

        # Prepare the data for insertion
        # Ensure these keys match your Supabase table column names
        data_to_insert = {
            "title": movie_data.get("title"),
            "releaseYear": movie_data.get("releaseYear"), # Adjust column name if different in DB
            "content": movie_data.get("content"),
            "embedding": embedding # This assumes your column for vectors is named 'embedding'
        }

        # Use upsert based on the 'title' column as the unique key
        # Adjust 'on_conflict' if you use a different unique constraint (e.g., 'id')
        response = await supabase.table(table_name).upsert(data_to_insert, on_conflict='title').execute()

        # Check response for errors
        if response and hasattr(response, 'error') and response.error:
             print(f"Error saving movie '{movie_data.get('title')}': {response.error}")
             return False # Indicate failure
        elif response:
             # print(f"Successfully saved/updated movie: {movie_data.get('title')}") # Optional success print
             return True # Indicate success
        else:
             print(f"Unknown response when saving movie '{movie_data.get('title')}'.")
             return False

    except Exception as e:
        print(f"Exception during save_movie_with_embedding for '{movie_data.get('title')}': {e}")
        return False # Indicate failure

# async def search_similar_movies(query_embedding: list):
#     ... (Implement this function later for recommendations) ...

# Optional: Keep or remove the local test block
# if __name__ == "__main__":
#    ...
