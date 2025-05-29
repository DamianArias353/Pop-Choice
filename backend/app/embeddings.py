import os
import openai

# Configure OpenAI API key from environment variables
# Ensure OPENAI_API_KEY is set in your .env file or environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# --- Add this print statement ---
print(f"DEBUG: OpenAI API Key found? {'Yes' if openai_api_key else 'No'}")
if openai_api_key:
    print(f"DEBUG: OpenAI API Key starts with: {openai_api_key[:5]}...") # Print first few chars
else:
    print("DEBUG: OpenAI API key not found, OpenAI client will not be initialized.")


# Initialize the OpenAI client with the API key
# The client must be initialized correctly BEFORE making API calls
if openai_api_key:
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        # print("DEBUG: OpenAI client initialized successfully.") # Keep or remove debug prints as needed
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        client = None
else:
    # print("DEBUG: OpenAI API key not found, OpenAI client will not be initialized.") # Keep or remove debug prints
    client = None


def get_embedding(text: str):
    """
    Generates an embedding for the given text using OpenAI's API (v1.0+ syntax).
    """
    if client is None:
        print("Error: OpenAI client not initialized. Cannot get embedding.")
        return None

    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

# Optional: Keep or remove the local test block if needed for direct file execution testing
# if __name__ == "__main__":
#     ...
