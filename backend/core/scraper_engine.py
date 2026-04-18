"""
Core scraping engine.

This module contains all the logic for:
    - Fetching HTML pages with retries and user‑agent rotation.
    - Parsing book data from HTML using BeautifulSoup.
    - Orchestrating concurrent page fetches with rate limiting.

The entry point is `scrape_all_pages()`, which returns a list of books.
"""

import requests
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .config import settings

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# Global User-Agent generator (reused for efficiency)
# -----------------------------------------------------------------------------
ua = UserAgent()

# -----------------------------------------------------------------------------
# Fetch Page with Retries
# -----------------------------------------------------------------------------
@retry(
    stop=stop_after_attempt(settings.scraper_config["retry_attempts"]),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.RequestException, ConnectionError))
)
def fetch_page(url: str) -> str:
    """
    Fetch a single URL's HTML content.

    Features:
        - Rotates User-Agent header to mimic different browsers.
        - Uses tenacity to retry on transient errors (network issues, timeouts).
        - Raises an exception if all retries fail.

    Args:
        url: The full URL to fetch.

    Returns:
        HTML content as a string.
    """
    # Build headers: rotate user-agent if enabled in config
    headers = {}
    if settings.scraper_config["user_agent_rotation"]:
        headers["User-Agent"] = ua.random
    else:
        headers["User-Agent"] = "Mozilla/5.0 (compatible; BookScraper/1.0; +http://example.com/bot)"

    logger.debug(f"Fetching {url} with User-Agent: {headers.get('User-Agent', 'default')}")
    
    resp = requests.get(
        url,
        headers=headers,
        timeout=settings.scraper_config["timeout"]
    )
    resp.raise_for_status()   # Raise HTTPError for bad status codes (4xx, 5xx)
    return resp.text

# -----------------------------------------------------------------------------
# Parse a Single Book Card
# -----------------------------------------------------------------------------
def parse_book_card(card_soup: BeautifulSoup) -> dict:
    """
    Extract book information from one product card (HTML element).

    The HTML structure of books.toscrape.com:
        <article class="product_pod">
            <h3><a title="Book Title">...</a></h3>
            <p class="price_color">£51.77</p>
            <p class="star-rating Four"></p>
            <p class="instock availability">In stock</p>
        </article>

    Args:
        card_soup: BeautifulSoup object representing a single book card.

    Returns:
        Dictionary with keys: title, price, rating, availability, upc.
        Returns None if parsing fails (errors are logged).
    """
    try:
        # Title: from the 'title' attribute of the <a> tag inside <h3>
        title_elem = card_soup.select_one("h3 a")
        title = title_elem["title"] if title_elem else "Unknown Title"

        # Price: text inside .price_color, e.g., "£51.77"
        price_elem = card_soup.select_one(".price_color")
        price_text = price_elem.text if price_elem else "£0.00"
        # Remove currency symbols and convert to float
        price = float(price_text.replace("£", "").replace("Â", ""))

        # Rating: the second class of the star-rating element (e.g., "Four")
        rating_elem = card_soup.select_one("p[class*=star-rating]")
        rating = rating_elem["class"][1] if rating_elem else "Zero"

        # Availability: text inside .instock
        availability_elem = card_soup.select_one(".instock")
        availability = availability_elem.text.strip() if availability_elem else "Out of stock"

        # UPC is not present on the listing page; we set a placeholder.
        # A more advanced scraper would follow the link to the product page.
        upc = "N/A"

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "upc": upc
        }
    except Exception as e:
        logger.error(f"Failed to parse book card: {e}")
        return None

# -----------------------------------------------------------------------------
# Parse a Full Page of Listings
# -----------------------------------------------------------------------------
def parse_listing(html: str) -> list:
    """
    Parse an HTML page containing multiple book cards.

    Args:
        html: Raw HTML content of a catalogue page.

    Returns:
        List of book dictionaries (each from parse_book_card).
        Empty list if no books found.
    """
    soup = BeautifulSoup(html, "lxml")
    book_cards = soup.select(".product_pod")
    books = []
    for card in book_cards:
        book = parse_book_card(card)
        if book:
            books.append(book)
    return books

# -----------------------------------------------------------------------------
# Main Scraping Orchestrator
# -----------------------------------------------------------------------------
def scrape_all_pages() -> list:
    """
    Main entry point for scraping.

    Steps:
        1. Generate URLs for all pages (from page 1 to max_pages).
        2. Use ThreadPoolExecutor to fetch multiple pages concurrently.
        3. For each completed fetch, parse the page and accumulate books.
        4. Add a random delay between completions to be polite to the server.
        5. Return the complete list of books.

    Returns:
        List of book dictionaries (all books from all pages).
    """
    # Load settings from configuration
    base_url = settings.scraper_config["base_url"]
    max_pages = settings.scraper_config["max_pages"]
    concurrency = settings.scraper_config["concurrency"]
    delay = settings.scraper_config["request_delay"]
    jitter = settings.scraper_config["request_jitter"]

    # Generate all page URLs (e.g., http://books.toscrape.com/catalogue/page-1.html)
    urls = [base_url.format(i) for i in range(1, max_pages + 1)]
    logger.info(f"Starting scrape of {len(urls)} pages with concurrency {concurrency}")

    all_books = []
    # ThreadPoolExecutor manages a pool of worker threads
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        # Submit all fetch tasks; future_to_url maps each Future to its URL
        future_to_url = {executor.submit(fetch_page, url): url for url in urls}

        # Iterate over completed futures as they finish
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                html = future.result()        # Get the HTML (may raise exception)
                books = parse_listing(html)   # Parse into book dicts
                all_books.extend(books)
                logger.info(f"Scraped {len(books)} books from {url}")
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {e}")

            # Polite delay: base delay + random jitter to avoid detection
            sleep_time = delay + random.uniform(0, jitter)
            time.sleep(sleep_time)

    logger.info(f"Scraping completed. Total books collected: {len(all_books)}")
    return all_books