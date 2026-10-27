"""Language catalog and validation service for Language Translation Tool."""

from typing import Dict, List, Any

# Standard ISO 639-1 language catalog with English and native names
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "native": "English"},
    "es": {"name": "Spanish", "native": "Español"},
    "fr": {"name": "French", "native": "Français"},
    "de": {"name": "German", "native": "Deutsch"},
    "it": {"name": "Italian", "native": "Italiano"},
    "pt": {"name": "Portuguese", "native": "Português"},
    "ru": {"name": "Russian", "native": "Русский"},
    "zh": {"name": "Chinese (Simplified)", "native": "中文 (简体)"},
    "ja": {"name": "Japanese", "native": "日本語"},
    "ko": {"name": "Korean", "native": "한국어"},
    "ar": {"name": "Arabic", "native": "العربية"},
    "hi": {"name": "Hindi", "native": "हिन्दी"},
    "bn": {"name": "Bengali", "native": "বাংলা"},
    "nl": {"name": "Dutch", "native": "Nederlands"},
    "pl": {"name": "Polish", "native": "Polski"},
    "tr": {"name": "Turkish", "native": "Türkçe"},
    "sv": {"name": "Swedish", "native": "Svenska"},
    "da": {"name": "Danish", "native": "Dansk"},
    "fi": {"name": "Finnish", "native": "Suomi"},
    "no": {"name": "Norwegian", "native": "Norsk"},
    "el": {"name": "Greek", "native": "Ελληνικά"},
    "cs": {"name": "Czech", "native": "Čeština"},
    "ro": {"name": "Romanian", "native": "Română"},
    "hu": {"name": "Hungarian", "native": "Magyar"},
    "uk": {"name": "Ukrainian", "native": "Українська"},
    "vi": {"name": "Vietnamese", "native": "Tiếng Việt"},
    "id": {"name": "Indonesian", "native": "Bahasa Indonesia"},
    "th": {"name": "Thai", "native": "ไทย"},
    "fa": {"name": "Persian", "native": "فارسی"},
    "he": {"name": "Hebrew", "native": "עברית"},
    "ur": {"name": "Urdu", "native": "اردو"},
    "sw": {"name": "Swahili", "native": "Kiswahili"},
}


class LanguageService:
    """Provides language catalog metadata and validation."""

    @classmethod
    def get_supported_languages(cls) -> Dict[str, Dict[str, str]]:
        """Returns the full dictionary of supported target/source languages."""
        return SUPPORTED_LANGUAGES

    @classmethod
    def get_language_list(cls) -> List[Dict[str, Any]]:
        """Returns language dictionary as a sorted list for dropdown population."""
        languages = [
            {"code": code, "name": data["name"], "native": data["native"]}
            for code, data in SUPPORTED_LANGUAGES.items()
        ]
        return sorted(languages, key=lambda x: x["name"])

    @classmethod
    def is_valid_source_language(cls, code: str) -> bool:
        """Validates if code is a supported source language or 'auto'."""
        if not code:
            return False
        normalized = code.lower().strip()
        return normalized == "auto" or normalized in SUPPORTED_LANGUAGES

    @classmethod
    def is_valid_target_language(cls, code: str) -> bool:
        """Validates if code is a supported target language (auto is not valid for target)."""
        if not code:
            return False
        normalized = code.lower().strip()
        return normalized in SUPPORTED_LANGUAGES

    @classmethod
    def get_language_name(cls, code: str) -> str:
        """Resolves ISO code to its English display name."""
        normalized = code.lower().strip()
        if normalized == "auto":
            return "Auto-Detect"
        if normalized in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[normalized]["name"]
        return code
