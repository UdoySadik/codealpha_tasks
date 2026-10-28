"""
tests/test_matcher.py
Unit tests for FAQMatcher TF-IDF vectorization, Cosine Similarity, and threshold filtering.
"""

import pytest
from src.config import AppConfig
from src.knowledge_base import FAQKnowledgeBase
from src.matcher import FAQMatcher, MatchResult
from src.preprocessor import TextPreprocessor


@pytest.fixture(scope="module")
def fitted_matcher():
    """Module-level fixture providing a fully fitted FAQMatcher."""
    kb = FAQKnowledgeBase("data/faqs.json")
    kb.load()
    preprocessor = TextPreprocessor()
    config = AppConfig.load_from_env()

    matcher = FAQMatcher(knowledge_base=kb, preprocessor=preprocessor, config=config)
    matcher.fit()
    return matcher


def test_unfitted_matcher_raises_runtime_error():
    """Verify RuntimeError is raised if match() is called prior to fit()."""
    kb = FAQKnowledgeBase("data/faqs.json")
    matcher = FAQMatcher(knowledge_base=kb)
    with pytest.raises(RuntimeError, match="must be fitted via fit()"):
        matcher.match("How do I register?")


def test_exact_canonical_match(fitted_matcher):
    """Verify exact canonical question matches with high confidence."""
    query = "How do I register for semester courses?"
    result = fitted_matcher.match(query)

    assert isinstance(result, MatchResult)
    assert result.status == "MATCH_FOUND"
    assert result.matched_faq is not None
    assert result.matched_faq.id == "faq_acad_001"
    assert result.confidence_score >= 0.85
    assert "Course registration is completed online" in result.answer


def test_paraphrased_queries_matching(fitted_matcher):
    """Verify natural conversational paraphrases match their expected FAQ items."""
    test_cases = [
        # (user query, expected_faq_id)
        ("Where can I pay my tuition bill?", "faq_fin_001"),
        ("I lost my student ID card, how do I get a new one?", "faq_card_002"),
        ("How do I connect to eduroam wireless on my phone?", "faq_it_001"),
        ("Can we reserve a study room in the library?", "faq_lib_002"),
        ("How do I order my official transcript for grad school?", "faq_acad_003"),
        ("Do students get free Microsoft Office 365?", "faq_it_003"),
    ]

    for query, expected_id in test_cases:
        res = fitted_matcher.match(query)
        assert res.status == "MATCH_FOUND", f"Failed for query: '{query}'"
        assert res.matched_faq is not None
        assert res.matched_faq.id == expected_id, (
            f"Query '{query}' matched '{res.matched_faq.id}', expected '{expected_id}'"
        )
        assert res.confidence_score >= 0.30


def test_out_of_domain_query_triggers_fallback(fitted_matcher):
    """Verify irrelevant / out-of-domain queries trigger the fallback response."""
    irrelevant_queries = [
        "How do I bake a chocolate cake at home?",
        "What is the capital of Australia?",
        "Who won the soccer match yesterday?",
        "Tell me a funny joke about cats.",
        "quantum physics black hole thermodynamics",
    ]

    for query in irrelevant_queries:
        res = fitted_matcher.match(query)
        assert res.status == "FALLBACK", f"Expected fallback for '{query}', got {res.status}"
        assert res.matched_faq is None
        assert "couldn't find a sufficiently relevant answer" in res.answer.lower()
        assert res.confidence_score < 0.30


def test_empty_and_whitespace_query_handling(fitted_matcher):
    """Verify empty or whitespace-only queries return EMPTY_QUERY status."""
    for empty_input in ["", "   ", "\t\n\r", "          "]:
        res = fitted_matcher.match(empty_input)
        assert res.status == "EMPTY_QUERY"
        assert res.matched_faq is None
        assert res.confidence_score == 0.0
        assert "Please enter a question" in res.answer


def test_pure_punctuation_query_handling(fitted_matcher):
    """Verify punctuation-only queries return EMPTY_QUERY."""
    for punct in ["???", "!!!!!", ".,.,.,", "???!@#$%^&*()"]:
        res = fitted_matcher.match(punct)
        assert res.status == "EMPTY_QUERY"
        assert res.matched_faq is None
        assert res.confidence_score == 0.0


def test_custom_threshold_override(fitted_matcher):
    """Verify that threshold override parameter dynamically alters matching behavior."""
    query = "Where do I obtain my campus ID card?"

    # With normal threshold (0.30) it matches
    normal_res = fitted_matcher.match(query, threshold_override=0.30)
    assert normal_res.status == "MATCH_FOUND"

    # With a strict threshold (0.95) a paraphrase must fallback
    strict_res = fitted_matcher.match(query, threshold_override=0.95)
    assert strict_res.status == "FALLBACK"

    # With an impossible threshold (> 1.0) any query must fallback
    impossible_res = fitted_matcher.match("Where can I get my student ID card?", threshold_override=1.01)
    assert impossible_res.status == "FALLBACK"

    # With a zero threshold it matches
    lenient_res = fitted_matcher.match(query, threshold_override=0.0)
    assert lenient_res.status == "MATCH_FOUND"


def test_confidence_score_bounded_range(fitted_matcher):
    """Verify confidence score is strictly bounded within [0.0, 1.0]."""
    queries = [
        "How do I register for semester courses?",
        "tuition fees",
        "xyz non-existent nonsense query 12345",
        "library books",
    ]
    for q in queries:
        res = fitted_matcher.match(q)
        assert 0.0 <= res.confidence_score <= 1.0
