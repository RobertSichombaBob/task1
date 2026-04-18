from backend.services.scraper_service import scraper_service

@router.post("/scrape", response_model=ScrapeTriggerResponse)
async def trigger_scrape(background_tasks: BackgroundTasks):
    def run_scrape():
        result = scraper_service.run_scraping_job()
        # You could store the result in a cache or send a notification
        print(f"Scrape result: {result}")
    
    background_tasks.add_task(run_scrape)
    return {"message": "Scraping started in background.", "books_scraped": 0}

@router.get("/books", response_model=List[BookResponse])
async def get_books(limit: int = 100, offset: int = 0):
    limit = min(limit, 500)
    books = scraper_service.get_all_books(limit, offset)
    return books

@router.get("/books/count")
async def get_book_count():
    return {"count": scraper_service.count_books()}