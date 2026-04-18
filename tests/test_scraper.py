"""
Unit tests for the scraping engine.

Tests cover:
    - HTML parsing of book cards
    - Handling of missing elements
    - Fetch page retry logic (mocked)
"""

import pytest
from bs4 import BeautifulSoup
from backend.core.scraper_engine import parse_book_card, parse_listing, fetch_page
from unittest.mock import patch, MagicMock

# -----------------------------------------------------------------------------
# Sample HTML for testing
# -----------------------------------------------------------------------------
SAMPLE_BOOK_CARD_HTML = """
<article class="product_pod">
    <h3><a title="The Great Gatsby">The Great Gatsby</a></h3>
    <p class="price_color">£12.99</p>
    <p class="star-rating Four"></p>
    <p class="instock">In stock</p>
</article>
"""

SAMPLE_LISTING_HTML = f"""
<html>
    <body>
        {SAMPLE_BOOK_CARD_HTML}
        {SAMPLE_BOOK_CARD_HTML.replace("The Great Gatsby", "1984")}
    </body>
</html>
"""

# -----------------------------------------------------------------------------
# Tests for parse_book_card
# -----------------------------------------------------------------------------
def test_parse_book_card_success():
    """Test parsing a valid book card."""
    soup = BeautifulSoup(SAMPLE_BOOK_CARD_HTML, "html.parser")
    book = parse_book_card(soup)
    
    assert book is not None
    assert book["title"] == "The Great Gatsby"
    assert book["price"] == 12.99
    assert book["rating"] == "Four"
    assert book["availability"] == "In stock"
    assert book["upc"] == "N/A"

def test_parse_book_card_missing_elements():
    """Test parsing a malformed card (missing title, price)."""
    html = """
    <article class="product_pod">
        <h3></h3>
        <p class="price_color"></p>
    </article>
    """
    soup = BeautifulSoup(html, "html.parser")
    book = parse_book_card(soup)
    
    # Should still return a dict with defaults (or None if critical error)
    # Our implementation returns None on exception; we expect None here.
    assert book is None

def test_parse_listing():
    """Test parsing a full page with multiple books."""
    books = parse_listing(SAMPLE_LISTING_HTML)
    assert len(books) == 2
    assert books[0]["title"] == "The Great Gatsby"
    assert books[1]["title"] == "1984"

# -----------------------------------------------------------------------------
# Tests for fetch_page (with mocking to avoid real network calls)
# -----------------------------------------------------------------------------
@patch("backend.core.scraper_engine.requests.get")
def test_fetch_page_success(mock_get):
    """Test successful page fetch."""
    mock_response = MagicMock()
    mock_response.text = "<html>Success</html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    html = fetch_page("http://example.com")
    assert html == "<html>Success</html>"

@patch("backend.core.scraper_engine.requests.get")
def test_fetch_page_retry_on_failure(mock_get):
    """Test that fetch_page retries on transient errors."""
    # First two calls raise exception, third succeeds
    mock_response = MagicMock()
    mock_response.text = "<html>Success</html>"
    mock_response.raise_for_status.return_value = None
    
    mock_get.side_effect = [
        ConnectionError("Timeout"),
        ConnectionError("Timeout"),
        mock_response
    ]
    
    html = fetch_page("http://example.com")
    assert html == "<html>Success</html>"
    assert mock_get.call_count == 3

@patch("backend.core.scraper_engine.requests.get")
def test_fetch_page_final_failure(mock_get):
    """Test that fetch_page raises after all retries fail."""
    mock_get.side_effect = ConnectionError("Always fails")
    
    with pytest.raises(ConnectionError):
        fetch_page("http://example.com")
    assert mock_get.call_count == 3  # Config says 3 attempts