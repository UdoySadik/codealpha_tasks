"""Development fallback translation provider.
Used for offline development, automated tests, and when no cloud API keys are configured.
Clearly and honestly marks all outputs with is_fallback=True.
"""

from typing import Dict
from providers.base import TranslationProvider, TranslationResult
from services.language_service import LanguageService

# Basic dictionary of common international greetings and terms for realistic dev testing
SAMPLE_DICTIONARY: Dict[str, Dict[str, str]] = {
    "hello": {
        "es": "Hola",
        "fr": "Bonjour",
        "de": "Hallo",
        "it": "Ciao",
        "pt": "Olá",
        "ru": "Привет",
        "zh": "你好",
        "ja": "こんにちは",
        "ko": "안녕하세요",
        "ar": "مرحبا",
        "hi": "नमस्ते",
        "bn": "হ্যালো",
    },
    "welcome": {
        "es": "Bienvenido",
        "fr": "Bienvenue",
        "de": "Willkommen",
        "it": "Benvenuto",
        "pt": "Bem-vindo",
        "ru": "Добро пожаловать",
        "zh": "欢迎",
        "ja": "ようこそ",
        "ko": "환영합니다",
        "ar": "أهلاً بك",
        "hi": "स्वागत हे",
        "bn": "স্বাগতম",
    },
    "thank you": {
        "es": "Gracias",
        "fr": "Merci",
        "de": "Danke",
        "it": "Grazie",
        "pt": "Obrigado",
        "ru": "Спасибо",
        "zh": "谢谢",
        "ja": "ありがとう",
        "ko": "감사합니다",
        "ar": "شكراً",
        "hi": "धन्यवाद",
        "bn": "ধন্যবাদ",
    },
}


class DevEchoFallbackProvider(TranslationProvider):
    """Local development fallback provider ensuring safe offline execution."""

    def __init__(self):
        super().__init__(provider_name="dev_fallback")

    def is_configured(self) -> bool:
        """Dev fallback is always available without credentials."""
        return True

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Generates deterministic development translation result."""
        clean_text = text.strip()
        lower_key = clean_text.lower()
        target_name = LanguageService.get_language_name(target_lang)

        # Check if text is a known sample phrase in our dictionary
        if lower_key in SAMPLE_DICTIONARY and target_lang in SAMPLE_DICTIONARY[lower_key]:
            translated_content = SAMPLE_DICTIONARY[lower_key][target_lang]
        else:
            # Clean simulated translation output for arbitrary text
            translated_content = f"[{target_name.upper()}]: {clean_text}"

        resolved_source = "en" if source_lang == "auto" else source_lang

        return TranslationResult(
            success=True,
            translated_text=translated_content,
            detected_source_lang=resolved_source,
            target_lang=target_lang,
            provider_name=self.provider_name,
            is_fallback=True,
            error_message=None,
        )
