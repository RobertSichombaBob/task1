"""
Pydantic models (schemas) for API request and response validation.

These define the shape of data that goes in and out of our API.
Using Pydantic ensures type safety and automatic documentation in Swagger.
"""

from pydantic import BaseModel, Field
from typing import Optional

# -----------------------------------------------------------------------------
# BookResponse: What a client receives when asking for a book.
# -----------------------------------------------------------------------------
class BookResponse(BaseModel):
    """
    Schema for a single book returned by the API.
    Matches the structure stored in our database (but omits the scraped_at timestamp).
    """
    id: int
    title: str
    price: float
    rating: str          # e.g., "One", "Two", ..., "Five"
    availability: str
    upc: Optional[str] = None   # Not always present in our simplified scraper

    class Config:
        orm_mode = True   # Allows automatic conversion from SQLite Row objects

# -----------------------------------------------------------------------------
# ScrapeTriggerResponse: Response after requesting a new scrape.
# -----------------------------------------------------------------------------
class ScrapeTriggerResponse(BaseModel):
    """
    Returned when the client calls POST /scrape.
    Contains a human-readable message and a placeholder for the number of books.
    (We don't know the count at the moment of response, so it's 0.)
    """
    message: str
    books_scraped: int = Field(0, description="Number of books scraped (0 initially, check later)")

# -----------------------------------------------------------------------------
# MessageResponse: Generic response for simple endpoints.
# -----------------------------------------------------------------------------
class MessageResponse(BaseModel):
    """
    Used for endpoints that just need to return a status message.
    """
    message: str
    status: Optional[str] = "ok"