from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as movies_router   # o el nombre que uses

app = FastAPI(
    title="PopChoice API",
    version="0.1.0",
)

# ─── CORS ───────────────────────────────────────────────────
origins = [
    "http://localhost:3000",     # Vite dev-server
    "https://tudominio.com",     # tu front en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # ["*"] si quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────

app.include_router(movies_router)

@app.get("/")
async def root():
    return {"message": "PopChoice backend is running"}