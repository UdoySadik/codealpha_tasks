"""
src/preprocessor.py
Deterministic NLP text normalization pipeline for the CodeAlpha FAQ Chatbot.

Performs lowercasing, punctuation removal, tokenization, stop-word filtering,
and WordNet morphological lemmatization.
"""

from __future__ import annotations

import re
from typing import List, Optional, Set
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TextPreprocessor:
    """
    Sanitizes, tokenizes, and lemmatizes raw natural language input strings.
    """

    def __init__(self, custom_stopwords: Optional[Set[str]] = None) -> None:
        self._ensure_nltk_corpora()
        self._lemmatizer = WordNetLemmatizer()

        # Load English stop words
        try:
            base_stopwords = set(stopwords.words("english"))
        except LookupError:
            base_stopwords = {
                "a", "an", "the", "in", "on", "at", "to", "for", "of", "with",
                "by", "is", "are", "was", "were", "be", "been", "being", "have",
                "has", "had", "do", "does", "did", "can", "could", "should", "would",
                "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her"
            }

        if custom_stopwords:
            self._stopwords = base_stopwords.union(custom_stopwords)
        else:
            self._stopwords = base_stopwords

        # Regex pattern matching alphanumeric tokens
        self._token_pattern = re.compile(r"\b[a-zA-Z0-9]+\b")

    @staticmethod
    def _ensure_nltk_corpora() -> None:
        """Quietly verify that required NLTK corpora are downloaded."""
        for corpus in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
            try:
                nltk.data.find(f"corpora/{corpus}")
            except LookupError:
                try:
                    nltk.data.find(f"tokenizers/{corpus}")
                except LookupError:
                    nltk.download(corpus, quiet=True)

    def tokenize(self, text: str) -> List[str]:
        """
        Extract word tokens from text after lowercasing.
        """
        if not text or not isinstance(text, str):
            return []
        lowered = text.lower()
        return self._token_pattern.findall(lowered)

    def lemmatize_token(self, token: str) -> str:
        """
        Morphologically lemmatize a single token as noun and verb.
        """
        # First attempt verb lemmatization (e.g. 'registering' -> 'register')
        verb_lemma = self._lemmatizer.lemmatize(token, pos="v")
        # Then attempt noun lemmatization on the result (e.g. 'fees' -> 'fee')
        return self._lemmatizer.lemmatize(verb_lemma, pos="n")

    def preprocess_tokens(self, text: str) -> List[str]:
        """
        Tokenize, strip punctuation, remove stop-words, and lemmatize tokens.

        Returns:
            List of normalized lemma tokens.
        """
        raw_tokens = self.tokenize(text)
        lemmas = []
        for token in raw_tokens:
            # Skip common stop words and purely non-alphanumeric noise
            if token not in self._stopwords and len(token) > 1:
                lemmatized = self.lemmatize_token(token)
                lemmas.append(lemmatized)
        return lemmas

    def preprocess(self, text: str) -> str:
        """
        Full end-to-end normalization pipeline returning a clean string.

        Args:
            text: Raw input string.

        Returns:
            Whitespace-joined normalized string (e.g., 'pay semester fee').
        """
        tokens = self.preprocess_tokens(text)
        return " ".join(tokens)


# Singleton preprocessor instance
DEFAULT_PREPROCESSOR = TextPreprocessor()
