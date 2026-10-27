"""Providers package exports."""

from providers.base import TranslationProvider, TranslationResult
from providers.fallback_provider import DevEchoFallbackProvider
from providers.mymemory_provider import MyMemoryProvider
from providers.google_provider import GoogleCloudProvider
from providers.azure_provider import AzureTranslatorProvider
from providers.deepl_provider import DeepLProvider

__all__ = [
    "TranslationProvider",
    "TranslationResult",
    "DevEchoFallbackProvider",
    "MyMemoryProvider",
    "GoogleCloudProvider",
    "AzureTranslatorProvider",
    "DeepLProvider",
]
