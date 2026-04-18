from fastapi import APIRouter, BackgroundTasks
from typing import List
from backend.core.database import db
from backend.api.models import BookResponse, ScrapeTriggerResponse, MessageResponse
from backend.services.scraper_service import scraper_service

# MUST have this line:
router = APIRouter()

@router.get("/books", response_model=List[BookResponse])
async def get_books(limit: int = 100, offset: int = 0):
    limit = min(limit, 500)
    return scraper_service.get_all_books(limit, offset)

@router.get("/books/count", response_model=dict)
async def get_book_count():
    return {"count": scraper_service.count_books()}

@router.post("/scrape", response_model=ScrapeTriggerResponse)
async def trigger_scrape(background_tasks: BackgroundTasks):
    def run_scrape():
        result = scraper_service.run_scraping_job()
        print(f"Scrape result: {result}")
    background_tasks.add_task(run_scrape)
    return {"message": "Scraping started in background.", "books_scraped": 0}

@router.get("/health", response_model=MessageResponse)
async def health_check():
    return {"message": "API is healthy", "status": "ok"}