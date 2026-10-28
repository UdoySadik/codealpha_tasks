"""
tests/test_preprocessor.py
Unit tests for TextPreprocessor NLP normalization, tokenization, and lemmatization.
"""

import pytest
from src.preprocessor import TextPreprocessor, DEFAULT_PREPROCESSOR


@pytest.fixture
def preprocessor():
    """Return default preprocessor fixture."""
    return DEFAULT_PREPROCESSOR


def test_basic_lowercasing_and_punctuation(preprocessor):
    """Verify lowercasing and punctuation removal."""
    raw = "HOW do I PAY my TUITION fees?!"
    processed = preprocessor.preprocess(raw)
    assert "pay" in processed
    assert "tuition" in processed
    assert "fee" in processed
    assert "?" not in processed
    assert "!" not in processed


def test_lemmatization_nouns_and_verbs(preprocessor):
    """Verify lemmatization of plurals and conjugated verbs."""
    # Noun plural to singular
    assert preprocessor.preprocess("books") == "book"
    assert preprocessor.preprocess("courses") == "course"
    assert preprocessor.preprocess("fees") == "fee"

    # Verb inflection to base form
    assert preprocessor.preprocess("registering") == "register"
    assert preprocessor.preprocess("enrolled") in ("enrol", "enroll")
    assert preprocessor.preprocess("paying") == "pay"


def test_stop_words_filtering(preprocessor):
    """Verify standard English stop words are filtered out."""
    raw = "What is the procedure for an official transcript?"
    processed = preprocessor.preprocess(raw)
    # "is", "the", "for", "an" should be filtered out
    tokens = processed.split()
    assert "procedure" in tokens
    assert "official" in tokens
    assert "transcript" in tokens
    assert "is" not in tokens
    assert "the" not in tokens
    assert "an" not in tokens


def test_numeric_preservation(preprocessor):
    """Verify numbers and alphanumeric codes are preserved."""
    assert "101" in preprocessor.preprocess("cs 101 course")
    assert "2026" in preprocessor.preprocess("academic year 2026")


def test_empty_and_whitespace_input(preprocessor):
    """Verify empty, whitespace, and purely punctuation inputs return empty string."""
    assert preprocessor.preprocess("") == ""
    assert preprocessor.preprocess("   ") == ""
    assert preprocessor.preprocess("\t\n") == ""
    assert preprocessor.preprocess("???!!!...,,,") == ""


def test_idempotence(preprocessor):
    """Verify that applying preprocessing twice yields identical result."""
    text = "How do I enroll in semester classes and pay fees?"
    first_pass = preprocessor.preprocess(text)
    second_pass = preprocessor.preprocess(first_pass)
    assert first_pass == second_pass
