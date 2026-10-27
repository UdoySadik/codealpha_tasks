"""Language Translation Tool — Main Application Server (Flask)."""

import os
from flask import Flask, jsonify, send_from_directory, request
from config import Config
from services.language_service import LanguageService
from services.translation_service import TranslationService

# Initialize Flask application with static file serving
app = Flask(__name__, static_folder="static")
app.config.from_object(Config)


@app.route("/", methods=["GET"])
def index():
    """Serves the single-page application frontend."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Returns the operational status and configuration of the translation service."""
    return jsonify({
        "status": "healthy",
        "service": "Language Translation Tool",
        "version": "1.0.0",
        "active_provider": Config.TRANSLATION_PROVIDER,
        "is_dev_fallback": Config.TRANSLATION_PROVIDER == "dev_fallback",
        "metadata": Config.get_public_metadata(),
    }), 200


@app.route("/api/languages", methods=["GET"])
def get_languages():
    """Returns the supported language list and dictionary."""
    return jsonify({
        "success": True,
        "count": len(LanguageService.get_supported_languages()),
        "languages": LanguageService.get_language_list(),
    }), 200


@app.route("/api/translate", methods=["POST"])
def translate():
    """Translates text from source language to target language.
    
    Expected JSON payload:
        {
            "text": "Hello world",
            "source_lang": "auto",   # or ISO 639-1 code
            "target_lang": "es"       # ISO 639-1 code
        }
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"success": False, "error": "Invalid JSON body provided."}), 400

    text = payload.get("text", "")
    source_lang = payload.get("source_lang", "auto")
    target_lang = payload.get("target_lang", "es")

    try:
        result = TranslationService.translate_text(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
        )

        status_code = 200 if result.get("success") else 502
        return jsonify(result), status_code

    except ValueError as val_err:
        return jsonify({"success": False, "error": str(val_err)}), 400
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred during translation.",
            "details": str(exc) if Config.DEBUG else None
        }), 500


@app.route("/api/tts", methods=["GET"])
def text_to_speech():
    """Streams Text-to-Speech audio for the requested text and language.
    Provides universal audio playback for all languages (including Bengali, Hindi, etc.)
    even when the client browser or OS has no local voice pack installed.
    """
    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "en").lower().strip()

    if not text:
        return jsonify({"success": False, "error": "No text provided for audio."}), 400

    clipped_text = text[:500]

    try:
        import io
        from flask import send_file
        from gtts import gTTS

        # Normalize language code for gTTS (e.g., 'zh' -> 'zh-CN')
        gtts_lang_map = {
            "zh": "zh-CN",
            "he": "iw",
        }
        resolved_lang = gtts_lang_map.get(lang, lang)

        tts = gTTS(text=clipped_text, lang=resolved_lang)
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        return send_file(audio_io, mimetype="audio/mpeg")

    except Exception as exc:
        # Graceful fallback to English audio if specific language not supported
        try:
            import io
            from flask import send_file
            from gtts import gTTS

            tts = gTTS(text=clipped_text, lang="en")
            audio_io = io.BytesIO()
            tts.write_to_fp(audio_io)
            audio_io.seek(0)
            return send_file(audio_io, mimetype="audio/mpeg")
        except Exception:
            return jsonify({"success": False, "error": "TTS audio generation failed."}), 500


@app.errorhandler(404)
def not_found_handler(error):
    """Graceful 404 handler for API routes and static assets."""
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404
    return send_from_directory(app.static_folder, "index.html")


@app.errorhandler(500)
def internal_error_handler(error):
    """Graceful 500 handler for unexpected exceptions."""
    return jsonify({"success": False, "error": "An internal server error occurred"}), 500


if __name__ == "__main__":
    print(f"[*] Starting Language Translation Tool on http://{Config.HOST}:{Config.PORT}")
    print(f"[*] Active Translation Provider: {Config.TRANSLATION_PROVIDER}")
    print(f"[*] Environment: {Config.APP_ENV} | Debug: {Config.DEBUG}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
