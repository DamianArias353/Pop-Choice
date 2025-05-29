from fastapi import FastAPI
from .routes import router # Import the router from routes.py
# No need to import get_embedding or get_movies directly here anymore

# Create FastAPI application instance
app = FastAPI()

# Include the router from routes.py
app.include_router(router)


# --- Root Endpoint (Optional - can also move to routes.py) ---
@app.get("/")
def read_root():
    return {"message": "PopChoice Backend API is running!"}