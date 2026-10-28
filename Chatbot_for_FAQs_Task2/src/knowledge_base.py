"""
src/knowledge_base.py
Knowledge Base repository and schema validator for the CodeAlpha FAQ Chatbot.

Loads structured FAQ data from JSON, validates schema integrity, and flattens
multi-pattern questions for downstream TF-IDF vector indexing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class FAQItem:
    """Represents a single canonical FAQ record."""

    id: str
    category: str
    question: str
    patterns: List[str]
    answer: str
    verified: bool = True
    notes: Optional[str] = None


@dataclass(frozen=True)
class IndexedPattern:
    """Represents a flattened pattern paired with its parent FAQ item."""

    pattern_text: str
    faq_id: str
    faq_item: FAQItem


class FAQKnowledgeBase:
    """
    Manages loading, validation, and retrieval of curated FAQ records.
    """

    REQUIRED_FIELDS: Set[str] = {"id", "category", "question", "patterns", "answer"}

    def __init__(self, data_path: Path | str) -> None:
        self.data_path = Path(data_path)
        self._faqs: Dict[str, FAQItem] = {}
        self._indexed_patterns: List[IndexedPattern] = []
        self._loaded: bool = False

    @property
    def is_loaded(self) -> bool:
        """Check if the knowledge base has been initialized and loaded."""
        return self._loaded

    @property
    def faqs(self) -> Dict[str, FAQItem]:
        """Return the dictionary of FAQ records indexed by ID."""
        return self._faqs

    @property
    def indexed_patterns(self) -> List[IndexedPattern]:
        """Return the list of flattened (pattern, FAQ) pairs."""
        return self._indexed_patterns

    def load(self) -> FAQKnowledgeBase:
        """
        Ingest the JSON file and validate record schema.

        Raises:
            FileNotFoundError: If the specified data path does not exist.
            ValueError: If JSON is malformed or records fail schema validation.
        """
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"FAQ knowledge base file not found at: {self.data_path.resolve()}"
            )

        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON format in {self.data_path}: {exc}") from exc

        if not isinstance(raw_data, list):
            raise ValueError(
                f"Expected top-level JSON list of FAQ items in {self.data_path}, got {type(raw_data).__name__}"
            )

        if not raw_data:
            raise ValueError(f"FAQ knowledge base at {self.data_path} is empty.")

        self._faqs.clear()
        self._indexed_patterns.clear()

        for idx, item in enumerate(raw_data):
            if not isinstance(item, dict):
                raise ValueError(f"FAQ record at index {idx} must be a JSON object.")

            missing_fields = self.REQUIRED_FIELDS - set(item.keys())
            if missing_fields:
                raise ValueError(
                    f"FAQ record at index {idx} missing required fields: {sorted(missing_fields)}"
                )

            faq_id = str(item["id"]).strip()
            if not faq_id:
                raise ValueError(f"FAQ record at index {idx} has an empty 'id'.")

            if faq_id in self._faqs:
                raise ValueError(f"Duplicate FAQ ID detected: '{faq_id}' at index {idx}.")

            patterns = item.get("patterns", [])
            if not isinstance(patterns, list) or not patterns:
                raise ValueError(
                    f"FAQ '{faq_id}' must define at least one pattern in 'patterns' list."
                )

            faq_obj = FAQItem(
                id=faq_id,
                category=str(item["category"]).strip(),
                question=str(item["question"]).strip(),
                patterns=[str(p).strip() for p in patterns if str(p).strip()],
                answer=str(item["answer"]).strip(),
                verified=bool(item.get("verified", True)),
                notes=item.get("notes"),
            )

            self._faqs[faq_id] = faq_obj

            # Index the canonical question itself
            self._indexed_patterns.append(
                IndexedPattern(pattern_text=faq_obj.question, faq_id=faq_id, faq_item=faq_obj)
            )

            # Index each paraphrased pattern
            for pattern in faq_obj.patterns:
                # Avoid duplicate indexing if canonical question is also in patterns
                if pattern.lower() != faq_obj.question.lower():
                    self._indexed_patterns.append(
                        IndexedPattern(pattern_text=pattern, faq_id=faq_id, faq_item=faq_obj)
                    )

        self._loaded = True
        return self

    def get_faq(self, faq_id: str) -> Optional[FAQItem]:
        """Retrieve a specific FAQ record by its unique ID."""
        return self._faqs.get(faq_id)

    def get_all_patterns(self) -> List[str]:
        """Extract all indexed pattern strings for vectorizer training."""
        return [ip.pattern_text for ip in self._indexed_patterns]

    def get_all_categories(self) -> List[str]:
        """Return a sorted list of unique categories in the knowledge base."""
        return sorted({faq.category for faq in self._faqs.values()})

    def count_faqs(self) -> int:
        """Return total number of unique FAQ items."""
        return len(self._faqs)

    def count_patterns(self) -> int:
        """Return total number of indexed question patterns."""
        return len(self._indexed_patterns)
