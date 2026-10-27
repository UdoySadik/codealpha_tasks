"""Centralized configuration module for the Language Translation Tool."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the task
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file if it exists
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Config:
    """Application configuration container."""

    # Server Settings
    APP_ENV: str = os.getenv("APP_ENV", "development").lower()
    DEBUG: bool = os.getenv("DEBUG", str(APP_ENV != "production")).lower() in ("true", "1", "yes")
    PORT: int = int(os.getenv("PORT", "5000"))
    HOST: str = os.getenv("HOST", "127.0.0.1")

    # Translation Provider
    TRANSLATION_PROVIDER: str = os.getenv("TRANSLATION_PROVIDER", "dev_fallback").lower().strip()

    # Google Cloud Translation Credentials
    GOOGLE_TRANSLATE_API_KEY: str | None = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    GOOGLE_APPLICATION_CREDENTIALS: str | None = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GOOGLE_CLOUD_PROJECT_ID: str | None = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    # Microsoft Azure Translator Credentials
    AZURE_TRANSLATOR_KEY: str | None = os.getenv("AZURE_TRANSLATOR_KEY")
    AZURE_TRANSLATOR_REGION: str = os.getenv("AZURE_TRANSLATOR_REGION", "eastus")
    AZURE_TRANSLATOR_ENDPOINT: str = os.getenv(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    ).rstrip("/")

    # DeepL API Credentials
    DEEPL_API_KEY: str | None = os.getenv("DEEPL_API_KEY")
    DEEPL_API_ENDPOINT: str = os.getenv(
        "DEEPL_API_ENDPOINT", "https://api-free.deepl.com/v2"
    ).rstrip("/")

    # MyMemory API Settings
    MYMEMORY_EMAIL: str | None = os.getenv("MYMEMORY_EMAIL")

    # Security & Limits
    MAX_CHARACTERS_PER_REQUEST: int = int(os.getenv("MAX_CHARACTERS_PER_REQUEST", "5000"))
    REQUEST_TIMEOUT_SECONDS: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    @classmethod
    def get_public_metadata(cls) -> dict:
        """Returns non-sensitive configuration metadata for UI & health checks."""
        return {
            "environment": cls.APP_ENV,
            "provider": cls.TRANSLATION_PROVIDER,
            "max_characters": cls.MAX_CHARACTERS_PER_REQUEST,
            "timeout_seconds": cls.REQUEST_TIMEOUT_SECONDS,
            "is_dev_fallback": cls.TRANSLATION_PROVIDER == "dev_fallback",
        }
