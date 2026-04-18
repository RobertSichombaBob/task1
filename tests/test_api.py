"""
Unit tests for FastAPI endpoints.

Tests cover:
    - Health check
    - GET /books (empty, with data, pagination)
    - GET /books/count
    - POST /scrape (background task simulation)
"""

import pytest
from unittest.mock import patch
from backend.core.database import db

# -----------------------------------------------------------------------------
# Helper to insert sample data
# -----------------------------------------------------------------------------
def insert_sample_books(sample_books):
    """Insert sample books into the test database."""
    for book in sample_books:
        # Remove id and scraped_at because they are auto-generated
        db.insert_books([{
            "title": book["title"],
            "price": book["price"],
            "rating": book["rating"],
            "availability": book["availability"],
            "upc": book.get("upc", "N/A")
        }])

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["message"] == "API is healthy"

def test_get_books_empty(client):
    """Test GET /books when database is empty."""
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    assert response.json() == []

def test_get_books_with_data(client, sample_books):
    """Test GET /books returns books after insertion."""
    insert_sample_books(sample_books)
    response = client.get("/api/v1/books?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Test Book 1"
    assert data[1]["title"] == "Test Book 2"

def test_get_books_pagination(client, sample_books):
    """Test pagination (limit and offset) works correctly."""
    # Insert more books (create 5 copies)
    for i in range(5):
        db.insert_books([{
            "title": f"Book {i}",
            "price": 10.0,
            "rating": "Three",
            "availability": "In stock",
            "upc": "N/A"
        }])
    
    response = client.get("/api/v1/books?limit=2&offset=0")
    assert len(response.json()) == 2
    
    response = client.get("/api/v1/books?limit=2&offset=2")
    assert len(response.json()) == 2

def test_get_book_count(client, sample_books):
    """Test GET /books/count returns correct number."""
    insert_sample_books(sample_books)
    response = client.get("/api/v1/books/count")
    assert response.status_code == 200
    assert response.json()["count"] == 2

@patch("backend.core.scraper_engine.scrape_all_pages")
def test_trigger_scrape(mock_scrape, client):
    """Test POST /scrape triggers background scraping."""
    mock_scrape.return_value = []  # Simulate no books found
    
    response = client.post("/api/v1/scrape")
    assert response.status_code == 200
    assert "Scraping started" in response.json()["message"]
    
    # Note: The background task runs asynchronously, so we can't easily assert
    # the result here. We rely on integration tests for that.