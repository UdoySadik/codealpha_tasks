"""Unit tests for TranslationService and LanguageService business logic."""

import pytest
from services.language_service import LanguageService
from services.translation_service import TranslationService
from providers.fallback_provider import DevEchoFallbackProvider
from providers.mymemory_provider import MyMemoryProvider


def test_language_service_catalog():
    """LanguageService must provide at least 32 verified languages."""
    catalog = LanguageService.get_supported_languages()
    assert len(catalog) >= 32
    assert "en" in catalog
    assert catalog["en"]["name"] == "English"
    assert catalog["es"]["native"] == "Español"


def test_language_service_validation():
    """Validates source and target language acceptance rules."""
    # Source allows 'auto' and known ISO codes
    assert LanguageService.is_valid_source_language("auto") is True
    assert LanguageService.is_valid_source_language("en") is True
    assert LanguageService.is_valid_source_language("EN") is True
    assert LanguageService.is_valid_source_language("  es  ") is True
    assert LanguageService.is_valid_source_language("") is False
    assert LanguageService.is_valid_source_language("fake_lang") is False

    # Target rejects 'auto', accepts known ISO codes
    assert LanguageService.is_valid_target_language("auto") is False
    assert LanguageService.is_valid_target_language("fr") is True
    assert LanguageService.is_valid_target_language("FR") is True
    assert LanguageService.is_valid_target_language("fake_lang") is False


def test_language_service_names():
    """Resolves language codes to correct display names."""
    assert LanguageService.get_language_name("auto") == "Auto-Detect"
    assert LanguageService.get_language_name("en") == "English"
    assert LanguageService.get_language_name("de") == "German"
    assert LanguageService.get_language_name("unknown") == "unknown"


def test_provider_factory_resolution():
    """TranslationService.get_provider returns the appropriate adapter instance."""
    p_dev = TranslationService.get_provider("dev_fallback")
    assert isinstance(p_dev, DevEchoFallbackProvider)

    p_mm = TranslationService.get_provider("mymemory")
    assert isinstance(p_mm, MyMemoryProvider)

    # When cloud provider has no credentials, factory safely returns dev fallback
    p_unconfigured = TranslationService.get_provider("google")
    assert isinstance(p_unconfigured, (DevEchoFallbackProvider,))


def test_translate_text_unicode_and_emojis():
    """Translation handles diverse Unicode characters and emojis gracefully."""
    unicode_text = "Hello! 🌍 বিশ্ব привет こんにちは"
    result = TranslationService.translate_text(
        text=unicode_text,
        source_lang="en",
        target_lang="es",
        provider_name="dev_fallback",
    )
    assert result["success"] is True
    assert unicode_text in result["translated_text"]


def test_translate_text_empty_raises_value_error():
    """Empty or whitespace text raises ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        TranslationService.translate_text("")

    with pytest.raises(ValueError, match="cannot be empty"):
        TranslationService.translate_text("    ")


def test_translate_text_length_exceeded_raises_value_error():
    """Oversized text raises ValueError."""
    with pytest.raises(ValueError, match="exceeds maximum"):
        TranslationService.translate_text("z" * 5001)


def test_translate_text_invalid_languages_raises():
    """Invalid language codes raise ValueError."""
    with pytest.raises(ValueError, match="source language"):
        TranslationService.translate_text("hello", source_lang="invalid_source")

    with pytest.raises(ValueError, match="target language"):
        TranslationService.translate_text("hello", target_lang="invalid_target")
