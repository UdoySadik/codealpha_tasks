"""DeepL API provider adapter.
Communicates with DeepL REST API v2.
"""

import html
import requests
from providers.base import TranslationProvider, TranslationResult
from config import Config


class DeepLProvider(TranslationProvider):
    """DeepL API client (Free and Pro)."""

    def __init__(self, api_key: str | None = None, endpoint: str | None = None):
        super().__init__(provider_name="deepl")
        self.api_key = api_key or Config.DEEPL_API_KEY
        self.endpoint = (endpoint or Config.DEEPL_API_ENDPOINT).rstrip("/")

    def is_configured(self) -> bool:
        """Returns True if DeepL auth key is configured."""
        return bool(self.api_key and self.api_key.strip())

    def _normalize_deepl_target(self, code: str) -> str:
        """Normalizes standard ISO code to DeepL target language requirements."""
        code_upper = code.upper()
        if code_upper == "EN":
            return "EN-US"
        if code_upper == "PT":
            return "PT-PT"
        return code_upper

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text via DeepL REST API."""
        if not self.is_configured():
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message="DeepL API key is not configured in .env",
            )

        url = f"{self.endpoint}/translate"
        headers = {
            "Authorization": f"DeepL-Auth-Key {self.api_key}",
            "Content-Type": "application/json",
        }

        target_normalized = self._normalize_deepl_target(target_lang)
        payload = {
            "text": [text],
            "target_lang": target_normalized,
        }
        if source_lang and source_lang != "auto":
            payload["source_lang"] = source_lang.upper()

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=Config.REQUEST_TIMEOUT_SECONDS,
            )
            response.encoding = "utf-8"

            if response.status_code in (401, 403):
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="DeepL authentication failed. Please verify DEEPL_API_KEY.",
                )

            if response.status_code == 456:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="DeepL translation quota exceeded.",
                )

            if response.status_code != 200:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message=f"DeepL API returned HTTP {response.status_code}",
                )

            data = response.json()
            translations = data.get("translations", [])
            if not translations:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="No translations returned by DeepL.",
                )

            first = translations[0]
            raw_text = first.get("text", "")
            detected = first.get("detected_source_language", "").lower()

            return TranslationResult(
                success=True,
                translated_text=html.unescape(raw_text),
                detected_source_lang=detected or (None if source_lang == "auto" else source_lang),
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
                error_message="DeepL translation request timed out.",
            )
        except requests.exceptions.RequestException as e:
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message=f"Network error connecting to DeepL: {str(e)}",
            )
