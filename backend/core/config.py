"""
Configuration management.

Loads settings from:
    1. config.yaml (YAML file)
    2. Environment variables (override YAML if present)

This allows easy customization without changing code.
"""

import yaml
from pathlib import Path
import os

class Settings:
    """
    Singleton class holding all configuration.
    Access properties like settings.scraper_config, settings.db_path, etc.
    """
    
    def __init__(self):
        # Locate config.yaml (one level above the backend folder)
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)
        
        # Override any YAML values with environment variables (if set)
        self._apply_env_overrides()

    def _apply_env_overrides(self):
        """
        Environment variables have higher priority than YAML.
        Map each environment variable to a YAML path and type conversion.
        """
        env_mapping = {
            "SCRAPER_MAX_PAGES": ("scraper", "max_pages", int),
            "SCRAPER_CONCURRENCY": ("scraper", "concurrency", int),
            "SCRAPER_REQUEST_DELAY": ("scraper", "request_delay", float),
            "SCRAPER_REQUEST_JITTER": ("scraper", "request_jitter", float),
            "SCRAPER_TIMEOUT": ("scraper", "timeout", int),
            "SCRAPER_RETRY_ATTEMPTS": ("scraper", "retry_attempts", int),
            "DATABASE_PATH": ("database", "sqlite_path", str),
            "LOG_LEVEL": ("logging", "level", str),
            "LOG_FILE": ("logging", "file", str),
        }
        for env_var, (section, key, cast) in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    self._config[section][key] = cast(value)
                except (ValueError, KeyError):
                    # If conversion fails or key doesn't exist, ignore and keep YAML value
                    pass

    # -------------------------------------------------------------------------
    # Properties to access specific parts of the configuration
    # -------------------------------------------------------------------------
    @property
    def scraper_config(self):
        """Dictionary with scraper settings: base_url, max_pages, concurrency, etc."""
        return self._config["scraper"]

    @property
    def db_path(self):
        """Path to the SQLite database file."""
        return self._config["database"]["sqlite_path"]

    @property
    def log_level(self):
        """Logging level (e.g., 'INFO', 'DEBUG')."""
        return self._config["logging"]["level"]

    @property
    def log_file(self):
        """File path where logs will be written."""
        return self._config["logging"]["file"]

# Create a global singleton instance. Other modules can do:
# from backend.core.config import settings
settings = Settings()