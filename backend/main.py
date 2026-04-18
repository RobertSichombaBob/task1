"""
FastAPI application entry point.
This module initializes the web server, sets up CORS, and includes the API routes.
It is the main process when running `uvicorn backend.main:app`.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import our route definitions and configuration
from backend.api.routes import router
from backend.core.config import settings

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
# We want both console output (StreamHandler) and a file (FileHandler)
# The log level (DEBUG, INFO, etc.) comes from config.yaml or environment.
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# FastAPI App Creation
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Book Scraper API",
    description="Scrape book data from books.toscrape.com and serve via REST",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc alternative
)

# -----------------------------------------------------------------------------
# CORS Middleware
# -----------------------------------------------------------------------------
# This allows our Streamlit frontend (running on a different port) to call our API.
# In production, restrict "allow_origins" to your actual frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Include API Routes
# -----------------------------------------------------------------------------
# All routes will be prefixed with /api/v1 (e.g., /api/v1/books)
app.include_router(router, prefix="/api/v1")

# -----------------------------------------------------------------------------
# Root Endpoint (Health Check)
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    """Simple health check to confirm API is running."""
    return {
        "message": "Book Scraper API is running. Go to /docs for Swagger documentation."
    }

# -----------------------------------------------------------------------------
# Startup and Shutdown Events
# -----------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """Log when the application starts, plus configuration summary."""
    logger.info("Starting Book Scraper API")
    logger.info(
        f"Configuration: max_pages={settings.scraper_config['max_pages']}, "
        f"concurrency={settings.scraper_config['concurrency']}"
    )

@app.on_event("shutdown")
async def shutdown_event():
    """Log when the application shuts down."""
    logger.info("Shutting down Book Scraper API")