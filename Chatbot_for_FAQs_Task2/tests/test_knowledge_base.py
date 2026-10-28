"""
tests/test_knowledge_base.py
Unit tests for FAQKnowledgeBase loading, schema validation, and pattern indexing.
"""

import json
from pathlib import Path
import pytest
from src.knowledge_base import FAQKnowledgeBase, FAQItem


@pytest.fixture
def default_kb():
    """Load default FAQ knowledge base fixture."""
    kb = FAQKnowledgeBase("data/faqs.json")
    kb.load()
    return kb


def test_load_default_faqs(default_kb):
    """Verify that default faqs.json loads successfully with required items."""
    assert default_kb.is_loaded is True
    assert default_kb.count_faqs() >= 20
    assert default_kb.count_patterns() >= 60

    categories = default_kb.get_all_categories()
    assert len(categories) >= 5
    assert "Academic Registration & Records" in categories
    assert "Tuition & Financial Services" in categories
    assert "Campus ID & Physical Access" in categories
    assert "Library & Academic Resources" in categories
    assert "Campus IT & Technical Support" in categories


def test_faq_record_schema_integrity(default_kb):
    """Verify that each FAQItem conforms to expected schema types."""
    for faq_id, faq in default_kb.faqs.items():
        assert isinstance(faq.id, str) and len(faq.id) > 0
        assert isinstance(faq.category, str) and len(faq.category) > 0
        assert isinstance(faq.question, str) and len(faq.question) > 0
        assert isinstance(faq.patterns, list) and len(faq.patterns) >= 1
        assert isinstance(faq.answer, str) and len(faq.answer) > 0
        assert isinstance(faq.verified, bool)


def test_get_faq_by_id(default_kb):
    """Verify retrieval of specific FAQ item by unique ID."""
    faq = default_kb.get_faq("faq_acad_001")
    assert faq is not None
    assert faq.id == "faq_acad_001"
    assert "register" in faq.question.lower()

    non_existent = default_kb.get_faq("non_existent_id")
    assert non_existent is None


def test_missing_file_raises_error():
    """Verify FileNotFoundError when data file does not exist."""
    kb = FAQKnowledgeBase("data/non_existent_faqs.json")
    with pytest.raises(FileNotFoundError, match="FAQ knowledge base file not found"):
        kb.load()


def test_corrupted_json_raises_error(tmp_path):
    """Verify ValueError when JSON file is syntax-invalid."""
    corrupted_file = tmp_path / "bad.json"
    corrupted_file.write_text("{ unclosed json: ", encoding="utf-8")

    kb = FAQKnowledgeBase(corrupted_file)
    with pytest.raises(ValueError, match="Invalid JSON format"):
        kb.load()


def test_missing_required_fields_raises_error(tmp_path):
    """Verify ValueError when FAQ item is missing required schema fields."""
    invalid_data = [{"id": "faq_bad_01", "question": "No answer or category"}]
    bad_file = tmp_path / "missing_fields.json"
    bad_file.write_text(json.dumps(invalid_data), encoding="utf-8")

    kb = FAQKnowledgeBase(bad_file)
    with pytest.raises(ValueError, match="missing required fields"):
        kb.load()


def test_duplicate_id_detection(tmp_path):
    """Verify ValueError when duplicate FAQ IDs are present."""
    duplicate_data = [
        {
            "id": "faq_dup",
            "category": "Test",
            "question": "Question 1",
            "patterns": ["p1"],
            "answer": "Answer 1",
        },
        {
            "id": "faq_dup",
            "category": "Test",
            "question": "Question 2",
            "patterns": ["p2"],
            "answer": "Answer 2",
        },
    ]
    dup_file = tmp_path / "dup.json"
    dup_file.write_text(json.dumps(duplicate_data), encoding="utf-8")

    kb = FAQKnowledgeBase(dup_file)
    with pytest.raises(ValueError, match="Duplicate FAQ ID detected"):
        kb.load()
