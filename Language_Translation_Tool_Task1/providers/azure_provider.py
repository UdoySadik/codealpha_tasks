"""Microsoft Azure Translator API provider adapter.
Communicates with Azure Cognitive Services Translator v3.0 REST endpoint.
"""

import html
import requests
from providers.base import TranslationProvider, TranslationResult
from config import Config


class AzureTranslatorProvider(TranslationProvider):
    """Microsoft Azure Translator v3.0 client."""

    def __init__(
        self,
        api_key: str | None = None,
        region: str | None = None,
        endpoint: str | None = None,
    ):
        super().__init__(provider_name="azure")
        self.api_key = api_key or Config.AZURE_TRANSLATOR_KEY
        self.region = region or Config.AZURE_TRANSLATOR_REGION
        self.endpoint = (endpoint or Config.AZURE_TRANSLATOR_ENDPOINT).rstrip("/")

    def is_configured(self) -> bool:
        """Returns True if Azure credentials are configured."""
        return bool(self.api_key and self.api_key.strip())

    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text via Azure Translator REST API."""
        if not self.is_configured():
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message="Azure Translator subscription key is not configured in .env",
            )

        url = f"{self.endpoint}/translate"
        params = {
            "api-version": "3.0",
            "to": target_lang,
        }
        if source_lang and source_lang != "auto":
            params["from"] = source_lang

        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Ocp-Apim-Subscription-Region": self.region,
            "Content-Type": "application/json",
        }
        body = [{"Text": text}]

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                json=body,
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
                    error_message="Azure Translator authentication failed. Please verify AZURE_TRANSLATOR_KEY and REGION.",
                )

            if response.status_code == 429:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="Azure Translator rate limit reached. Please wait a moment.",
                )

            if response.status_code != 200:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message=f"Azure Translator returned HTTP {response.status_code}",
                )

            data = response.json()
            if not isinstance(data, list) or len(data) == 0:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="Malformed response received from Azure Translator.",
                )

            first_item = data[0]
            translations = first_item.get("translations", [])
            if not translations:
                return TranslationResult(
                    success=False,
                    translated_text="",
                    detected_source_lang=None,
                    target_lang=target_lang,
                    provider_name=self.provider_name,
                    is_fallback=False,
                    error_message="No translation item in Azure response.",
                )

            translated_text = translations[0].get("text", "")
            detected_lang = first_item.get("detectedLanguage", {}).get("language")

            return TranslationResult(
                success=True,
                translated_text=html.unescape(translated_text),
                detected_source_lang=detected_lang or (None if source_lang == "auto" else source_lang),
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
                error_message="Azure Translator request timed out.",
            )
        except requests.exceptions.RequestException as e:
            return TranslationResult(
                success=False,
                translated_text="",
                detected_source_lang=None,
                target_lang=target_lang,
                provider_name=self.provider_name,
                is_fallback=False,
                error_message=f"Network error connecting to Azure Translator: {str(e)}",
            )
