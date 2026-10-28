"""
tests/test_config.py
Unit tests for AppConfig configuration management and validation.
"""

import os
from pathlib import Path
import pytest
from src.config import AppConfig, DEFAULT_CONFIG


def test_default_config_values():
    """Verify default configuration attributes are correctly populated."""
    config = AppConfig.load_from_env()

    assert isinstance(config.faq_data_path, Path)
    assert config.faq_data_path == Path("data/faqs.json")
    assert isinstance(config.similarity_threshold, float)
    assert config.similarity_threshold == 0.30
    assert "rephrase" in config.fallback_message.lower()
    assert "empty" in config.empty_input_message.lower()
    assert config.log_level == "INFO"


def test_singleton_default_config_instance():
    """Verify DEFAULT_CONFIG singleton is available and valid."""
    assert DEFAULT_CONFIG is not None
    assert DEFAULT_CONFIG.similarity_threshold == 0.30


def test_immutable_config():
    """Verify that AppConfig is frozen against attribute mutation."""
    config = AppConfig.load_from_env()
    with pytest.raises(Exception):
        # Attempting to mutate a frozen dataclass must raise FrozenInstanceError
        config.similarity_threshold = 0.50  # type: ignore


def test_custom_environment_threshold(monkeypatch):
    """Verify environment variable overrides for similarity threshold."""
    monkeypatch.setenv("SIMILARITY_THRESHOLD", "0.45")
    config = AppConfig.load_from_env()
    assert config.similarity_threshold == 0.45


def test_invalid_environment_threshold_fallback(monkeypatch):
    """Verify fallback to 0.30 if environment threshold is non-numeric or out-of-range."""
    monkeypatch.setenv("SIMILARITY_THRESHOLD", "not_a_number")
    config = AppConfig.load_from_env()
    assert config.similarity_threshold == 0.30

    monkeypatch.setenv("SIMILARITY_THRESHOLD", "1.50")
    config = AppConfig.load_from_env()
    assert config.similarity_threshold == 0.30

    monkeypatch.setenv("SIMILARITY_THRESHOLD", "-0.10")
    config = AppConfig.load_from_env()
    assert config.similarity_threshold == 0.30


def test_custom_data_path(monkeypatch):
    """Verify custom FAQ data path override."""
    monkeypatch.setenv("FAQ_DATA_PATH", "custom/path/faqs.json")
    config = AppConfig.load_from_env()
    assert config.faq_data_path == Path("custom/path/faqs.json")
