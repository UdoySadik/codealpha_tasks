"""
src/config.py
Configuration management for the CodeAlpha FAQ Chatbot.

Defines runtime hyperparameters, system messages, similarity thresholds,
and file path configurations with defensive validation and environment variable overrides.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration dataclass."""

    # Path to the JSON knowledge base file
    faq_data_path: Path

    # Minimum cosine similarity score (0.0 to 1.0) to qualify as a valid match
    similarity_threshold: float

    # System fallback response when no candidate reaches similarity_threshold
    fallback_message: str

    # Message returned when the user submits an empty or whitespace query
    empty_input_message: str

    # Application display metadata
    app_title: str
    app_subtitle: str
    log_level: str

    @classmethod
    def load_from_env(cls, env_path: Optional[str] = None) -> AppConfig:
        """
        Factory method to construct AppConfig from environment variables with safe defaults.
        """
        if env_path:
            load_dotenv(dotenv_path=env_path, override=True)

        raw_path = os.getenv("FAQ_DATA_PATH", "data/faqs.json")
        faq_data_path = Path(raw_path)

        raw_threshold = os.getenv("SIMILARITY_THRESHOLD", "0.30")
        try:
            similarity_threshold = float(raw_threshold)
            if not 0.0 <= similarity_threshold <= 1.0:
                similarity_threshold = 0.30
        except ValueError:
            similarity_threshold = 0.30

        fallback_message = os.getenv(
            "DEFAULT_FALLBACK_MESSAGE",
            "I'm sorry, but I couldn't find a sufficiently relevant answer in the FAQ database "
            "for your question. Could you please rephrase or reach out to student support?",
        )

        empty_input_message = os.getenv(
            "EMPTY_INPUT_MESSAGE",
            "Please enter a question. The query cannot be empty or contain only whitespace.",
        )

        app_title = os.getenv("APP_TITLE", "🎓 Campus Services FAQ Assistant")
        app_subtitle = os.getenv(
            "APP_SUBTITLE",
            "Instant answers to questions on academic registrations, tuition, student IDs, and campus services.",
        )

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        return cls(
            faq_data_path=faq_data_path,
            similarity_threshold=similarity_threshold,
            fallback_message=fallback_message,
            empty_input_message=empty_input_message,
            app_title=app_title,
            app_subtitle=app_subtitle,
            log_level=log_level,
        )


# Singleton default configuration instance
DEFAULT_CONFIG = AppConfig.load_from_env()
