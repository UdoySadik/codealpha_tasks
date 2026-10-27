"""Pytest configuration and shared test fixtures."""

import sys
from pathlib import Path
import pytest

# Ensure the task directory is on sys.path
TASK_DIR = Path(__file__).resolve().parent.parent
if str(TASK_DIR) not in sys.path:
    sys.path.insert(0, str(TASK_DIR))

from app import app as flask_app
from config import Config


@pytest.fixture(autouse=True)
def isolated_test_config(monkeypatch):
    """Isolates testing config from local developer .env values."""
    monkeypatch.setattr(Config, "TRANSLATION_PROVIDER", "dev_fallback")
    monkeypatch.setattr(Config, "GOOGLE_TRANSLATE_API_KEY", "")
    monkeypatch.setattr(Config, "AZURE_TRANSLATOR_KEY", "")
    monkeypatch.setattr(Config, "DEEPL_API_KEY", "")


@pytest.fixture
def app():
    """Provides the Flask application instance configured for testing."""
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    return flask_app


@pytest.fixture
def client(app):
    """Provides a test client for dispatching HTTP requests against the app."""
    return app.test_client()


@pytest.fixture
def sample_payload():
    """Provides a standard valid translation request payload."""
    return {
        "text": "Hello world",
        "source_lang": "en",
        "target_lang": "es",
    }
