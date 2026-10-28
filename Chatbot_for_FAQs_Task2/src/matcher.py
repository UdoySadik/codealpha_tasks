"""
src/matcher.py
Vector-space Information Retrieval and Cosine Similarity Matching Engine.

Transforms normalized FAQ questions into TF-IDF representations and calculates
cosine similarity to identify the most relevant FAQ answer with threshold filtering
and fallback logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import AppConfig, DEFAULT_CONFIG
from src.knowledge_base import FAQItem, FAQKnowledgeBase
from src.preprocessor import TextPreprocessor, DEFAULT_PREPROCESSOR


@dataclass(frozen=True)
class MatchResult:
    """Encapsulates the output of a query similarity evaluation."""

    query: str
    normalized_query: str
    matched_faq: Optional[FAQItem]
    matched_pattern: Optional[str]
    confidence_score: float
    status: str  # "MATCH_FOUND", "FALLBACK", "EMPTY_QUERY"
    answer: str


class FAQMatcher:
    """
    TF-IDF Vector Space information retrieval matcher with configurable threshold.
    """

    def __init__(
        self,
        knowledge_base: FAQKnowledgeBase,
        preprocessor: Optional[TextPreprocessor] = None,
        config: Optional[AppConfig] = None,
    ) -> None:
        self.kb = knowledge_base
        self.preprocessor = preprocessor or DEFAULT_PREPROCESSOR
        self.config = config or DEFAULT_CONFIG

        self._vectorizer: Optional[TfidfVectorizer] = None
        self._tfidf_matrix: Optional[np.ndarray] = None
        self._indexed_patterns = []
        self._is_fitted: bool = False

    @property
    def is_fitted(self) -> bool:
        """Check if vectorizer has been fitted on corpus patterns."""
        return self._is_fitted

    def fit(self) -> FAQMatcher:
        """
        Preprocess all FAQ pattern variants and fit the TfidfVectorizer.

        Returns:
            Self instance after fitting.
        """
        if not self.kb.is_loaded:
            self.kb.load()

        self._indexed_patterns = self.kb.indexed_patterns
        raw_patterns = [ip.pattern_text for ip in self._indexed_patterns]

        # Apply preprocessing to all training patterns
        normalized_corpus = [
            self.preprocessor.preprocess(pattern) for pattern in raw_patterns
        ]

        # Use unigram and bigram representation with L2 normalization
        self._vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            norm="l2",
            sublinear_tf=True,
        )

        self._tfidf_matrix = self._vectorizer.fit_transform(normalized_corpus)
        self._is_fitted = True
        return self

    def match(
        self,
        query: str,
        threshold_override: Optional[float] = None,
    ) -> MatchResult:
        """
        Evaluate a user query against the fitted vector space.

        Args:
            query: Raw user question string.
            threshold_override: Optional custom threshold to override config.

        Returns:
            MatchResult containing answer, confidence score, and status.
        """
        if not self._is_fitted or self._vectorizer is None or self._tfidf_matrix is None:
            raise RuntimeError("FAQMatcher must be fitted via fit() before calling match().")

        threshold = (
            threshold_override
            if threshold_override is not None
            else self.config.similarity_threshold
        )

        # 1. Intercept empty or whitespace-only queries
        if not query or not query.strip():
            return MatchResult(
                query=query or "",
                normalized_query="",
                matched_faq=None,
                matched_pattern=None,
                confidence_score=0.0,
                status="EMPTY_QUERY",
                answer=self.config.empty_input_message,
            )

        # 2. Preprocess query
        normalized_query = self.preprocessor.preprocess(query)

        # If preprocessing eliminates all tokens (e.g. purely symbols '???'), return empty input notice
        if not normalized_query.strip():
            return MatchResult(
                query=query,
                normalized_query="",
                matched_faq=None,
                matched_pattern=None,
                confidence_score=0.0,
                status="EMPTY_QUERY",
                answer=self.config.empty_input_message,
            )

        # 3. Analyze query tokens and vocabulary coverage
        query_tokens = self.preprocessor.preprocess_tokens(query)
        vocab = self._vectorizer.vocabulary_
        in_vocab_tokens = [t for t in query_tokens if t in vocab]

        # If zero query tokens exist in vocabulary, return fallback immediately
        if not in_vocab_tokens:
            return MatchResult(
                query=query,
                normalized_query=normalized_query,
                matched_faq=None,
                matched_pattern=None,
                confidence_score=0.0,
                status="FALLBACK",
                answer=self.config.fallback_message,
            )

        # Calculate coverage ratio: proportion of query content words recognized in the FAQ corpus
        coverage_ratio = len(in_vocab_tokens) / len(query_tokens)

        # 4. Transform query into TF-IDF vector
        query_vector = self._vectorizer.transform([normalized_query])

        # 5. Compute Cosine Similarity against all indexed pattern vectors
        similarities = cosine_similarity(query_vector, self._tfidf_matrix).flatten()

        # 6. Identify candidate with highest similarity score
        best_idx = int(np.argmax(similarities))
        raw_score = float(similarities[best_idx])

        # Scale similarity score by query term coverage to dampen queries with high OOV ratio
        final_score = raw_score * coverage_ratio
        final_score = max(0.0, min(1.0, round(final_score, 4)))

        # 7. Apply similarity threshold
        if final_score >= threshold:
            best_candidate = self._indexed_patterns[best_idx]
            return MatchResult(
                query=query,
                normalized_query=normalized_query,
                matched_faq=best_candidate.faq_item,
                matched_pattern=best_candidate.pattern_text,
                confidence_score=final_score,
                status="MATCH_FOUND",
                answer=best_candidate.faq_item.answer,
            )
        else:
            return MatchResult(
                query=query,
                normalized_query=normalized_query,
                matched_faq=None,
                matched_pattern=None,
                confidence_score=final_score,
                status="FALLBACK",
                answer=self.config.fallback_message,
            )
