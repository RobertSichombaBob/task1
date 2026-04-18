"""
SQLite database interface.

Handles:
    - Creating the database and tables if they don't exist.
    - Inserting scraped books.
    - Retrieving books with pagination.
    - Counting books.

Uses a context manager for connections to ensure proper closing.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, Any
import logging

from .config import settings

logger = logging.getLogger(__name__)

class Database:
    """
    Database wrapper for SQLite.
    
    All database operations go through this class.
    It is a singleton (only one instance created) to avoid multiple connections.
    """
    
    def __init__(self):
        self.db_path = settings.db_path
        # Ensure the directory for the database exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()
        logger.info(f"Database initialized at {self.db_path}")

    def _init_tables(self):
        """
        Create the 'books' table if it doesn't exist.
        Also creates an index on the 'title' column for faster searches.
        """
        with self.get_connection() as conn:
            # Books table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    price REAL,
                    rating TEXT,
                    availability TEXT,
                    upc TEXT,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Index for faster title-based queries (if we add search later)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON books(title)")

    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Usage:
            with db.get_connection() as conn:
                conn.execute(...)
        
        This guarantees that the connection is properly closed after use,
        and that any exception triggers a rollback.
        """
        conn = sqlite3.connect(self.db_path)
        # Row factory makes rows behave like dictionaries
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database transaction failed: {e}")
            raise
        finally:
            conn.close()

    def insert_books(self, books: List[Dict[str, Any]]):
        """
        Insert a list of book dictionaries into the database.
        
        Args:
            books: List of dicts with keys: title, price, rating, availability, upc
        """
        if not books:
            return
        
        with self.get_connection() as conn:
            for book in books:
                try:
                    conn.execute("""
                        INSERT INTO books (title, price, rating, availability, upc)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        book["title"],
                        book["price"],
                        book["rating"],
                        book["availability"],
                        book.get("upc", "N/A")
                    ))
                except Exception as e:
                    logger.error(f"Failed to insert book {book.get('title')}: {e}")
        
        logger.info(f"Inserted {len(books)} books into database")

    def get_all_books(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Retrieve a paginated list of books, ordered by most recent first.
        
        Args:
            limit: Maximum number of books to return.
            offset: Number of books to skip (for pagination).
        
        Returns:
            List of dictionaries, each representing a book.
        """
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, title, price, rating, availability, upc, scraped_at
                FROM books
                ORDER BY id DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            return [dict(row) for row in cursor.fetchall()]

    def count_books(self) -> int:
        """Return the total number of books stored in the database."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM books")
            return cursor.fetchone()["count"]

    def delete_all_books(self):
        """
        Delete all books from the table.
        Useful for testing or resetting the database.
        """
        with self.get_connection() as conn:
            conn.execute("DELETE FROM books")
        logger.warning("All books deleted from database")

# Global database instance. Other modules can do:
# from backend.core.database import db
db = Database()