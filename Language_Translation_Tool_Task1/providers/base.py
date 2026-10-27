"""Abstract Base Class and data models for translation providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationResult:
    """Standardized translation output model."""
    success: bool
    translated_text: str
    detected_source_lang: Optional[str]
    target_lang: str
    provider_name: str
    is_fallback: bool
    error_message: Optional[str] = None

    def to_dict(self) -> dict:
        """Converts result dataclass to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "translated_text": self.translated_text,
            "detected_source_lang": self.detected_source_lang,
            "target_lang": self.target_lang,
            "provider": self.provider_name,
            "is_fallback": self.is_fallback,
            "error": self.error_message,
        }


class TranslationProvider(ABC):
    """Abstract interface that all translation provider adapters must implement."""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    def is_configured(self) -> bool:
        """Checks if required API keys or credentials are present."""
        pass

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> TranslationResult:
        """Translates text from source_lang to target_lang."""
        pass
