"""Integration tests for Flask application routes and API endpoints."""

import json
from config import Config


def test_index_page_returns_200(client):
    """GET / must return HTTP 200 and serve HTML containing PolyGlot branding."""
    response = client.get("/")
    assert response.status_code == 200
    html_content = response.data.decode("utf-8")
    assert "PolyGlot AI" in html_content
    assert "translation-workspace" in html_content


def test_static_css_and_js_served(client):
    """Static assets must return HTTP 200."""
    css_res = client.get("/static/css/style.css")
    assert css_res.status_code == 200
    assert len(css_res.data) > 0

    js_app = client.get("/static/js/app.js")
    assert js_app.status_code == 200

    js_langs = client.get("/static/js/languages.js")
    assert js_langs.status_code == 200


def test_health_check_endpoint(client):
    """GET /api/health must report operational readiness and active provider."""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "Language Translation Tool"
    assert "active_provider" in data
    assert "metadata" in data
    assert data["metadata"]["max_characters"] == Config.MAX_CHARACTERS_PER_REQUEST


def test_languages_endpoint(client):
    """GET /api/languages must return 30+ supported languages."""
    response = client.get("/api/languages")
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["count"] >= 30
    assert isinstance(data["languages"], list)

    # Verify presence of major languages
    codes = [l["code"] for l in data["languages"]]
    assert "en" in codes
    assert "es" in codes
    assert "fr" in codes
    assert "de" in codes
    assert "zh" in codes
    assert "ja" in codes
    assert "ar" in codes
    assert "bn" in codes


def test_translate_valid_text_dev_fallback(client):
    """POST /api/translate with valid text returns translation result."""
    payload = {
        "text": "Good morning",
        "source_lang": "en",
        "target_lang": "es",
    }
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert "translated_text" in data
    assert len(data["translated_text"]) > 0
    assert data["target_lang"] == "es"


def test_translate_dictionary_greeting(client):
    """POST /api/translate with sample greeting returns localized translation."""
    payload = {
        "text": "hello",
        "source_lang": "en",
        "target_lang": "es",
    }
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["translated_text"] == "Hola"


def test_translate_same_language_short_circuit(client):
    """Translating identical source and target language returns original text immediately."""
    payload = {
        "text": "Identical text content",
        "source_lang": "es",
        "target_lang": "es",
    }
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["translated_text"] == "Identical text content"
    assert data["provider"] == "identical_languages"


def test_translate_empty_text_returns_400(client):
    """Submitting empty string must return HTTP 400 Bad Request."""
    response = client.post("/api/translate", json={"text": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "empty" in data["error"].lower()


def test_translate_whitespace_only_returns_400(client):
    """Submitting whitespace-only string must return HTTP 400."""
    response = client.post("/api/translate", json={"text": "   \n\t  "})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "empty" in data["error"].lower()


def test_translate_non_json_body_returns_400(client):
    """Submitting non-JSON raw body must return HTTP 400."""
    response = client.post(
        "/api/translate",
        data="not a json string",
        content_type="text/plain",
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False


def test_translate_exceeds_max_characters_returns_400(client):
    """Submitting text exceeding 5,000 characters must return HTTP 400."""
    long_text = "x" * (Config.MAX_CHARACTERS_PER_REQUEST + 1)
    response = client.post("/api/translate", json={"text": long_text})
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "exceeds" in data["error"].lower()


def test_translate_exact_max_characters_accepted(client):
    """Submitting text of exactly 5,000 characters must be accepted."""
    exact_text = "y" * Config.MAX_CHARACTERS_PER_REQUEST
    response = client.post("/api/translate", json={"text": exact_text, "source_lang": "en", "target_lang": "fr"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True


def test_translate_invalid_source_language_returns_400(client):
    """Submitting unsupported source language code returns HTTP 400."""
    payload = {"text": "hello", "source_lang": "nonexistent_code", "target_lang": "es"}
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "invalid" in data["error"].lower()


def test_translate_invalid_target_language_returns_400(client):
    """Submitting unsupported target language code returns HTTP 400."""
    payload = {"text": "hello", "source_lang": "en", "target_lang": "invalid_code"}
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "invalid" in data["error"].lower()


def test_translate_auto_target_disallowed(client):
    """Target language cannot be 'auto'."""
    payload = {"text": "hello", "source_lang": "en", "target_lang": "auto"}
    response = client.post("/api/translate", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False


def test_api_not_found_returns_json_404(client):
    """Requesting an unknown /api/* route returns clean JSON 404."""
    response = client.get("/api/unsupported_route")
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
    assert "not found" in data["error"].lower()


def test_tts_empty_text_returns_400(client):
    """GET /api/tts without text parameter returns HTTP 400."""
    response = client.get("/api/tts?text=&lang=en")
    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert "no text" in data["error"].lower()


def test_tts_valid_request_returns_audio_stream(client):
    """GET /api/tts with valid parameters returns 200 audio/mpeg binary stream."""
    response = client.get("/api/tts?text=hello&lang=en")
    assert response.status_code == 200
    assert response.content_type.startswith("audio/mpeg")
    assert len(response.data) > 0


def test_tts_bengali_audio_stream(client):
    """GET /api/tts for Bengali returns 200 audio/mpeg binary stream."""
    response = client.get("/api/tts?text=dhonnobad&lang=bn")
    assert response.status_code == 200
    assert response.content_type.startswith("audio/mpeg")
    assert len(response.data) > 0
