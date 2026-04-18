"""
API Client for Streamlit frontend.

This module handles all communication with the FastAPI backend.
It provides functions to:
    - Trigger a new scraping job.
    - Fetch books (paginated).
    - Get total book count.
"""

import requests
import streamlit as st
from typing import List, Dict, Any

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# For local development (without Docker), use localhost.
# If you use Docker, change to "http://backend:8000/api/v1"
API_BASE_URL = "http://localhost:8000/api/v1"

# -----------------------------------------------------------------------------
# API Functions
# -----------------------------------------------------------------------------
def trigger_scrape() -> Dict[str, Any]:
    """
    Send a POST request to start a scraping job in the background.

    Returns:
        Dictionary with 'message' and 'books_scraped' (always 0 initially).
    """
    try:
        response = requests.post(f"{API_BASE_URL}/scrape", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to trigger scrape: {e}")
        return {"message": str(e), "books_scraped": 0}

def fetch_books(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Retrieve a paginated list of books from the backend.

    Args:
        limit: Maximum number of books to return (capped by backend at 500).
        offset: Number of books to skip (for pagination).

    Returns:
        List of book dictionaries, each with keys: id, title, price, rating, etc.
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/books",
            params={"limit": limit, "offset": offset},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch books: {e}")
        return []

def fetch_book_count() -> int:
    """
    Get the total number of books stored in the database.

    Returns:
        Integer count, or 0 if the request fails.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/books/count", timeout=10)
        response.raise_for_status()
        return response.json().get("count", 0)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch book count: {e}")
        return 0

def health_check() -> bool:
    """
    Check if the backend API is reachable and healthy.

    Returns:
        True if healthy, False otherwise.
    """
    try:
        # The health endpoint is at root level, not under /api/v1
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False