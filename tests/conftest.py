"""
pytest configuration and shared fixtures.

This file provides reusable fixtures for testing:
    - FastAPI test client
    - Sample book data
    - Temporary database for isolated tests
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.database import db
import tempfile
import os

# -----------------------------------------------------------------------------
# Fixture: FastAPI test client
# -----------------------------------------------------------------------------
@pytest.fixture
def client():
    """Return a TestClient for the FastAPI application."""
    return TestClient(app)

# -----------------------------------------------------------------------------
# Fixture: Sample book data
# -----------------------------------------------------------------------------
@pytest.fixture
def sample_books():
    """Provide a list of sample book dictionaries for testing."""
    return [
        {
            "id": 1,
            "title": "Test Book 1",
            "price": 19.99,
            "rating": "Four",
            "availability": "In stock",
            "upc": "1234567890",
            "scraped_at": "2024-01-01 12:00:00"
        },
        {
            "id": 2,
            "title": "Test Book 2",
            "price": 29.99,
            "rating": "Five",
            "availability": "In stock",
            "upc": "0987654321",
            "scraped_at": "2024-01-01 12:01:00"
        }
    ]

# -----------------------------------------------------------------------------
# Fixture: Temporary database for isolated tests
# -----------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    """
    Override the database path to a temporary file for each test.
    This ensures tests don't affect the real database.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        temp_db_path = tmp.name
    
    # Patch the db.db_path to use the temporary file
    monkeypatch.setattr("backend.core.database.settings.db_path", temp_db_path)
    
    # Reinitialize the database singleton with the new path
    from backend.core.database import Database
    global db
    db.__init__ = Database.__init__
    db._init_tables()
    
    yield temp_db_path
    
    # Cleanup
    os.unlink(temp_db_path)