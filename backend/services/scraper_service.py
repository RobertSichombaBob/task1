"""
Scraper Service Layer.

This module provides a high-level interface for:
    - Executing scraping jobs (with progress tracking and error handling)
    - Fetching scraped data from the database
    - Counting books

It acts as a bridge between the API routes and the core scraping/database modules.
All business logic related to scraping coordination lives here.
"""

import logging
from typing import List, Dict, Any, Optional

from backend.core.scraper_engine import scrape_all_pages
from backend.core.database import db

logger = logging.getLogger(__name__)

class ScraperService:
    """
    Service class for scraping operations.
    
    This class encapsulates all scraping-related business logic.
    It is stateless and can be used as a singleton.
    """
    
    @staticmethod
    def run_scraping_job() -> Dict[str, Any]:
        """
        Execute a full scraping job: fetch all pages, parse books, and store them.

        This is the main entry point for triggering a scrape from the API.
        It handles:
            - Calling the scraping engine
            - Inserting results into the database
            - Returning a summary of what happened

        Returns:
            Dictionary with:
                - success (bool): Whether the job completed without fatal errors.
                - books_scraped (int): Number of books successfully scraped.
                - message (str): Human-readable status message.
        """
        logger.info("Scraping job started.")
        
        try:
            # 1. Perform the scraping (this may take several seconds)
            books = scrape_all_pages()
            
            # 2. Store results if any books were found
            if books:
                db.insert_books(books)
                logger.info(f"Scraping job completed: {len(books)} books inserted.")
                return {
                    "success": True,
                    "books_scraped": len(books),
                    "message": f"Successfully scraped and stored {len(books)} books."
                }
            else:
                logger.warning("Scraping job completed but no books were found.")
                return {
                    "success": True,
                    "books_scraped": 0,
                    "message": "Scraping completed, but no books were extracted. Check the website or selectors."
                }
        except Exception as e:
            logger.error(f"Scraping job failed: {e}", exc_info=True)
            return {
                "success": False,
                "books_scraped": 0,
                "message": f"Scraping failed: {str(e)}"
            }
    
    @staticmethod
    def get_all_books(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retrieve a paginated list of books from the database.

        This is a simple passthrough to the database layer, but it exists
        here to maintain a clean service interface. Future enhancements
        (e.g., filtering, sorting) can be added here without changing API routes.

        Args:
            limit: Max number of books to return.
            offset: Number of books to skip.

        Returns:
            List of book dictionaries.
        """
        return db.get_all_books(limit, offset)
    
    @staticmethod
    def count_books() -> int:
        """
        Get the total number of books stored in the database.

        Returns:
            Integer count.
        """
        return db.count_books()
    
    @staticmethod
    def delete_all_books() -> int:
        """
        Delete all books from the database (useful for testing or resetting).

        Returns:
            Number of books deleted (before deletion).
        """
        count_before = db.count_books()
        db.delete_all_books()
        logger.info(f"Deleted {count_before} books from database.")
        return count_before

# -----------------------------------------------------------------------------
# Convenience singleton instance
# -----------------------------------------------------------------------------
# Other modules can import this instance directly, e.g.:
# from backend.services.scraper_service import scraper_service
scraper_service = ScraperService()