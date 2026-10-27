"""Unit tests for individual Translation Provider adapters using mocked responses."""

from unittest.mock import patch, MagicMock
import requests

from providers import (
    DevEchoFallbackProvider,
    MyMemoryProvider,
    GoogleCloudProvider,
    AzureTranslatorProvider,
    DeepLProvider,
)


# --- 1. DevEchoFallbackProvider Tests ---

def test_dev_fallback_provider():
    """Fallback provider always reports configured and flags is_fallback=True."""
    provider = DevEchoFallbackProvider()
    assert provider.is_configured() is True

    # Test dictionary match
    res_greeting = provider.translate("hello", "en", "es")
    assert res_greeting.success is True
    assert res_greeting.translated_text == "Hola"
    assert res_greeting.is_fallback is True

    # Test non-dictionary arbitrary text
    res_arbitrary = provider.translate("Antigravity IDE", "en", "fr")
    assert res_arbitrary.success is True
    assert "[FRENCH]: Antigravity IDE" in res_arbitrary.translated_text
    assert res_arbitrary.is_fallback is True


# --- 2. MyMemoryProvider Tests ---

@patch("requests.get")
def test_mymemory_success(mock_get):
    """MyMemory parses successful JSON response correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "responseStatus": 200,
        "responseData": {"translatedText": "Hola mundo"},
    }
    mock_get.return_value = mock_response

    provider = MyMemoryProvider()
    result = provider.translate("Hello world", "en", "es")

    assert result.success is True
    assert result.translated_text == "Hola mundo"
    assert result.is_fallback is False


@patch("requests.get")
def test_mymemory_timeout(mock_get):
    """MyMemory handles network timeout gracefully."""
    mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

    provider = MyMemoryProvider()
    result = provider.translate("Hello world", "en", "es")

    assert result.success is False
    assert "timed out" in result.error_message.lower()


# --- 3. GoogleCloudProvider Tests ---

def test_google_unconfigured():
    """Unconfigured Google provider returns clear error."""
    provider = GoogleCloudProvider(api_key=None)
    assert provider.is_configured() is False

    result = provider.translate("hello", "en", "es")
    assert result.success is False
    assert "not configured" in result.error_message.lower()


@patch("requests.post")
def test_google_success_unescapes_html(mock_post):
    """Google provider unescapes HTML entities in translation text."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "translations": [
                {
                    "translatedText": "&quot;Bonjour le monde&quot;",
                    "detectedSourceLanguage": "en",
                }
            ]
        }
    }
    mock_post.return_value = mock_response

    provider = GoogleCloudProvider(api_key="test_dummy_key")
    result = provider.translate('"Hello world"', "en", "fr")

    assert result.success is True
    assert result.translated_text == '"Bonjour le monde"'
    assert result.detected_source_lang == "en"


@patch("requests.post")
def test_google_auth_failure(mock_post):
    """Google provider handles HTTP 403 authentication / billing error."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_post.return_value = mock_response

    provider = GoogleCloudProvider(api_key="invalid_key")
    result = provider.translate("hello", "en", "es")

    assert result.success is False
    assert "authentication failed" in result.error_message.lower()


# --- 4. AzureTranslatorProvider Tests ---

def test_azure_unconfigured():
    """Unconfigured Azure provider returns clear error."""
    provider = AzureTranslatorProvider(api_key=None)
    assert provider.is_configured() is False

    result = provider.translate("hello", "en", "es")
    assert result.success is False
    assert "not configured" in result.error_message.lower()


@patch("requests.post")
def test_azure_success(mock_post):
    """Azure provider parses translation array correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "detectedLanguage": {"language": "en"},
            "translations": [{"text": "Hallo Welt"}],
        }
    ]
    mock_post.return_value = mock_response

    provider = AzureTranslatorProvider(api_key="dummy_azure_key", region="eastus")
    result = provider.translate("Hello world", "auto", "de")

    assert result.success is True
    assert result.translated_text == "Hallo Welt"
    assert result.detected_source_lang == "en"


# --- 5. DeepLProvider Tests ---

def test_deepl_target_normalization():
    """DeepL normalizes target codes (e.g., en -> EN-US, pt -> PT-PT)."""
    provider = DeepLProvider(api_key="dummy:fx")
    assert provider._normalize_deepl_target("en") == "EN-US"
    assert provider._normalize_deepl_target("pt") == "PT-PT"
    assert provider._normalize_deepl_target("es") == "ES"


@patch("requests.post")
def test_deepl_success(mock_post):
    """DeepL provider parses translation response correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "translations": [
            {
                "text": "Bonjour tout le monde",
                "detected_source_language": "EN",
            }
        ]
    }
    mock_post.return_value = mock_response

    provider = DeepLProvider(api_key="dummy_deepl_key:fx")
    result = provider.translate("Hello everyone", "en", "fr")

    assert result.success is True
    assert result.translated_text == "Bonjour tout le monde"
    assert result.detected_source_lang == "en"


@patch("requests.post")
def test_deepl_quota_exceeded(mock_post):
    """DeepL provider handles HTTP 456 quota exceeded."""
    mock_response = MagicMock()
    mock_response.status_code = 456
    mock_post.return_value = mock_response

    provider = DeepLProvider(api_key="dummy_key:fx")
    result = provider.translate("test", "en", "de")

    assert result.success is False
    assert "quota exceeded" in result.error_message.lower()
