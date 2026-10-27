"""MyMemory Free Translation Provider implementation.
Provides genuine public API translation without requiring a paid cloud subscription.
"""

import html
import requests
from providers.base import TranslationProvider, TranslationResult
from config import Config


class MyMemoryProvider(TranslationProvider):
    """MyMemory Translated API client."""

    API_ENDPOINT = "https://api.mymemory.translated.net/get"

    def __init__(self, email: str | None = None):
        super().__init__(provider_name="mymemory")
        self.email = email or Config.MYMEMORY_EMAIL

    def is_configured(self) -> bool:
        """MyMemory is usable anonymously without credentials."""
        return True

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text via MyMemory REST API."""
        src = "autodetect" if source_lang == "auto" else source_lang
        langpair = f"{src}|{target_lang}"

        params = {
            "q": text,
            "langpair": langpair,
        }
        if self.email:
            params["de"] = self.email

        try:
            response = requests.get(
                self.API_ENDPOINT,
                params=params,
                timeout=Config.REQUEST_TIMEOUT_SECONDS,
            )
            response.encoding = "utf-8"

            if response.status_code != 200:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message=f"MyMemory API returned HTTP {response.status_code}",
                )

            data = response.json()
            status = data.get("responseStatus")

            if status != 200:
                details = data.get("responseDetails", "Translation error from provider")
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message=details,
                )

            raw_translated = data.get("responseData", {}).get("translatedText", "")
            # Unescape any HTML entities returned by MyMemory
            cleaned_text = html.unescape(raw_translated)

            return TranslationResult(
                success=True,
                translated_text=cleaned_text,
                detected_source_lang=None if source_lang == "auto" else source_lang,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message=None,
            )

        except requests.exceptions.Timeout:
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message="MyMemory translation request timed out (10s limit).",
            )
        except requests.exceptions.RequestException as e:
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message=f"Network error connecting to MyMemory: {str(e)}",
            )
