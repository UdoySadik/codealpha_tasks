"""Google Cloud Translation API provider adapter.
Communicates with Google Cloud Translation Basic v2 REST endpoint.
"""

import html
import requests
from providers.base import TranslationProvider, TranslationResult
from config import Config


class GoogleCloudProvider(TranslationProvider):
    """Google Cloud Translation API v2 client."""

    API_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"

    def __init__(self, api_key: str | None = None):
        super().__init__(provider_name="google")
        self.api_key = api_key or Config.GOOGLE_TRANSLATE_API_KEY

    def is_configured(self) -> bool:
        """Returns True if Google Cloud API key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text via Google Cloud Translation API."""
        if not self.is_configured():
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message="Google Cloud Translation API key is not configured in .env",
            )

        payload = {
            "q": text,
            "target": target_lang,
            "format": "text",
        }
        if source_lang and source_lang != "auto":
            payload["source"] = source_lang

        try:
            response = requests.post(
                self.API_ENDPOINT,
                params={"key": self.api_key},
                json=payload,
                timeout=Config.REQUEST_TIMEOUT_SECONDS,
            )
            response.encoding = "utf-8"

            if response.status_code == 403:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="Google Cloud Translation API authentication failed or billing inactive.",
                )

            if response.status_code == 429:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="Google Cloud Translation rate limit reached. Please retry in a moment.",
                )

            if response.status_code != 200:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message=f"Google Cloud Translation error: HTTP {response.status_code}",
                )

            data = response.json()
            translations = data.get("data", {}).get("translations", [])
            if not translations:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="Empty translation returned by Google Cloud API.",
                )

            first = translations[0]
            raw_text = first.get("translatedText", "")
            detected_lang = first.get("detectedSourceLanguage") or (None if source_lang == "auto" else source_lang)

            return TranslationResult(
                success=True,
                translated_text=html.unescape(raw_text),
                detected_source_lang=detected_lang,
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
                error_message="Google Cloud Translation request timed out.",
            )
        except requests.exceptions.RequestException as e:
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message=f"Network error connecting to Google Cloud Translation: {str(e)}",
            )
