from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api import router
from app.utils.logging import configure_logging
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root (not backend folder)
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

# Check for demo mode
import os
demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"

if demo_mode:
    print("\n✅ DEMO MODE ENABLED - Using mock services (no API keys required)\n")
else:
    # Verify critical keys are loaded
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  WARNING: OPENAI_API_KEY not set in .env")
    if not os.getenv("PINECONE_API_KEY"):
        print("⚠️  WARNING: PINECONE_API_KEY not set in .env")

configure_logging()

app = FastAPI(
    title="IKMS RAG API",
    version="1.0.0",
    description="Evidence-Aware RAG System with PDF Indexing and Citation Support",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Enable CORS for local development and frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve static files (HTML UI)
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "IKMS RAG API is running"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "qa": "/qa",
            "search": "/search",
            "index_pdf": "/index-pdf",
            "upload_pdf": "/upload-pdf",
            "docs": "/docs",
            "ui": "/static/index.html"
        }
    }
