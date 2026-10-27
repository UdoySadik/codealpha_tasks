"""Translation orchestrator service.
Manages provider resolution, input validation, and translation dispatching.
"""

import logging
from config import Config
from services.language_service import LanguageService
from providers import (
    TranslationProvider,
    DevEchoFallbackProvider,
    MyMemoryProvider,
    GoogleCloudProvider,
    AzureTranslatorProvider,
    DeepLProvider,
)

logger = logging.getLogger(__name__)


class TranslationService:
    """Core translation business logic and provider factory."""

    @classmethod
    def get_provider(cls, requested_name: str | None = None) -> TranslationProvider:
        """Instantiates and returns the configured translation provider adapter."""
        name = (requested_name or Config.TRANSLATION_PROVIDER).lower().strip()

        if name == "google":
            provider = GoogleCloudProvider()
            if provider.is_configured():
                return provider
            logger.warning("[!] Google Cloud requested but not configured; engaging dev fallback.")
            return DevEchoFallbackProvider()

        if name == "azure":
            provider = AzureTranslatorProvider()
            if provider.is_configured():
                return provider
            logger.warning("[!] Azure Translator requested but not configured; engaging dev fallback.")
            return DevEchoFallbackProvider()

        if name == "deepl":
            provider = DeepLProvider()
            if provider.is_configured():
                return provider
            logger.warning("[!] DeepL requested but not configured; engaging dev fallback.")
            return DevEchoFallbackProvider()

        if name == "mymemory":
            return MyMemoryProvider()

        # Default fallback provider
        return DevEchoFallbackProvider()

    @classmethod
    def translate_text(
        cls,
        text: str,
        source_lang: str = "auto",
        target_lang: str = "es",
        provider_name: str | None = None,
    ) -> dict:
        """Validates inputs and dispatches translation to active provider."""
        # 1. Validate text presence
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        stripped_text = text.strip()

        # 2. Validate max character limit
        if len(stripped_text) > Config.MAX_CHARACTERS_PER_REQUEST:
            raise ValueError(
                f"Input text exceeds maximum allowed limit of {Config.MAX_CHARACTERS_PER_REQUEST} characters."
            )

        # 3. Validate language codes
        normalized_source = (source_lang or "auto").lower().strip()
        normalized_target = (target_lang or "es").lower().strip()

        if not LanguageService.is_valid_source_language(normalized_source):
            raise ValueError(f"Invalid or unsupported source language code: '{source_lang}'")

        if not LanguageService.is_valid_target_language(normalized_target):
            raise ValueError(f"Invalid or unsupported target language code: '{target_lang}'")

        # 4. Same source and target short-circuit
        if normalized_source != "auto" and normalized_source == normalized_target:
            return {
                "success": True,
                "translated_text": stripped_text,
                "detected_source_lang": normalized_source,
                "target_lang": normalized_target,
                "provider": "identical_languages",
                "is_fallback": False,
                "error": None,
            }

        # 5. Resolve active provider and dispatch translation
        provider = cls.get_provider(provider_name)
        result = provider.translate(
            text=stripped_text,
            source_lang=normalized_source,
            target_lang=normalized_target,
        )

        return result.to_dict()
