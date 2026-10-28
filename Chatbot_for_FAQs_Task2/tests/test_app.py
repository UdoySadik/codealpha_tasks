"""
tests/test_app.py
Functional integration tests verifying app.py module components and engine caching.
"""

import pytest
from app import load_faq_matcher
from src.config import DEFAULT_CONFIG


def test_app_engine_loader_success():
    """Verify load_faq_matcher correctly loads and fits FAQMatcher."""
    matcher, err = load_faq_matcher(str(DEFAULT_CONFIG.faq_data_path))
    assert err is None
    assert matcher is not None
    assert matcher.is_fitted is True
    assert matcher.kb.count_faqs() >= 20


def test_app_engine_loader_missing_file():
    """Verify load_faq_matcher gracefully catches errors on invalid paths."""
    matcher, err = load_faq_matcher("data/non_existent_file.json")
    assert matcher is None
    assert err is not None
    assert "not found" in err.lower()


def test_app_end_to_end_query_pipeline():
    """Verify query pipeline as utilized within app.py."""
    matcher, err = load_faq_matcher(str(DEFAULT_CONFIG.faq_data_path))
    assert matcher is not None

    # Simulate query submitted via chat input
    query = "How do I register for semester courses?"
    res = matcher.match(query, threshold_override=0.30)
    assert res.status == "MATCH_FOUND"
    assert "Course registration" in res.answer
    assert res.matched_faq.category == "Academic Registration & Records"
