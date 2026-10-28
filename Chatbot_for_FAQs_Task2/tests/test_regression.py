"""
tests/test_regression.py
Full dataset regression tests verifying 100% of canonical questions and pattern variations.
"""

import json
from pathlib import Path
import pytest
from src.config import AppConfig
from src.knowledge_base import FAQKnowledgeBase
from src.matcher import FAQMatcher
from src.preprocessor import TextPreprocessor

# Load dataset once for test parameterization
FAQS_PATH = Path("data/faqs.json")
with open(FAQS_PATH, "r", encoding="utf-8") as f:
    ALL_FAQS = json.load(f)

CANONICAL_CASES = [(faq["question"], faq["id"]) for faq in ALL_FAQS]

ALL_PATTERN_CASES = [
    (pattern, faq["id"])
    for faq in ALL_FAQS
    for pattern in faq.get("patterns", [])
]


@pytest.fixture(scope="module")
def matcher():
    """Module-level fitted FAQMatcher fixture."""
    kb = FAQKnowledgeBase("data/faqs.json")
    kb.load()
    preprocessor = TextPreprocessor()
    config = AppConfig.load_from_env()

    m = FAQMatcher(knowledge_base=kb, preprocessor=preprocessor, config=config)
    m.fit()
    return m


@pytest.mark.parametrize("canonical_question,expected_faq_id", CANONICAL_CASES)
def test_canonical_question_regression(matcher, canonical_question, expected_faq_id):
    """
    Verify every canonical FAQ question in the database retrieves its exact FAQ intent.
    Confidence score must be high (>= 0.70).
    """
    res = matcher.match(canonical_question)
    assert res.status == "MATCH_FOUND", (
        f"Canonical query failed to match: '{canonical_question}'"
    )
    assert res.matched_faq is not None
    assert res.matched_faq.id == expected_faq_id, (
        f"Canonical query '{canonical_question}' mapped to '{res.matched_faq.id}', expected '{expected_faq_id}'"
    )
    assert res.confidence_score >= 0.70, (
        f"Score too low ({res.confidence_score}) for canonical question '{canonical_question}'"
    )


@pytest.mark.parametrize("pattern_text,expected_faq_id", ALL_PATTERN_CASES)
def test_pattern_variation_regression(matcher, pattern_text, expected_faq_id):
    """
    Verify every paraphrased pattern variation in the database retrieves its parent FAQ intent.
    Confidence score must meet or exceed the similarity threshold (>= 0.30).
    """
    res = matcher.match(pattern_text)
    assert res.status == "MATCH_FOUND", (
        f"Pattern variation failed to match: '{pattern_text}'"
    )
    assert res.matched_faq is not None
    assert res.matched_faq.id == expected_faq_id, (
        f"Pattern '{pattern_text}' mapped to '{res.matched_faq.id}', expected '{expected_faq_id}'"
    )
    assert res.confidence_score >= 0.30, (
        f"Score too low ({res.confidence_score}) for pattern '{pattern_text}'"
    )
