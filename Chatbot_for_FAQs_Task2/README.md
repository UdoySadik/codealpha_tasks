# 🤖 Intelligent FAQ Chatbot

> **CodeAlpha Artificial Intelligence Internship — Task Submission Project**  
> **Status:** Fully Implemented, Verified & Tested (146/146 Automated Tests Passing)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-1.66-FF4B4B.svg)](https://streamlit.io/)
[![NLP](https://img.shields.io/badge/NLTK-WordNet%20%7C%20Stopwords-green.svg)](https://www.nltk.org/)
[![ML](https://img.shields.io/badge/scikit--learn-TF--IDF%20%7C%20Cosine%20Similarity-orange.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/pytest-146%20Passed%20(100%25)-brightgreen.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📌 Project Overview

The **Intelligent FAQ Chatbot** is a deterministic, lightweight, and privacy-preserving Natural Language Processing (NLP) conversational agent designed for university student academic and campus services.

Rather than relying on uncalibrated, costly, or hallucination-prone cloud LLMs, this system implements an industrial-grade **Information Retrieval (IR) Vector Space Model**. It cleans and lemmatizes natural-language queries, converts them into mathematical representations via **TF-IDF (Term Frequency-Inverse Document Frequency)**, and calculates vector alignment using **Cosine Similarity with Query Term Coverage Weighting**.

If an incoming question fails to reach the calibrated similarity threshold ($\tau = 0.30$), the system safely falls back to a polite guidance message instead of serving false or misleading answers.

---

## 🎯 Key Features & Capabilities

- **Curated Campus Knowledge Base**: 22 curated FAQ topics across 5 categories with 88 natural-language paraphrases.
- **NLP Preprocessing Pipeline**: Tokenization, punctuation removal, case-folding, stop-word elimination, and morphological WordNet lemmatization.
- **Coverage-Weighted Vector Matching**: Sublinear TF scaling, bigram capture (`ngram_range=(1,2)`), $L_2$ normalized vector representations, and cosine similarity scaled by vocabulary coverage to safely filter out accidental keyword matches.
- **Configurable Fallback Threshold**: Tunable cutoff threshold ($\tau = 0.30$) preventing false positives on out-of-domain queries.
- **Responsive Streamlit Web Interface**: Deep Slate & Indigo theme, welcoming hero card, clickable suggestion chips, message timeline with avatars (`🧑‍🎓` / `🤖`), match confidence chips, and a conversation reset control.
- **Zero Cloud / Paid API Dependencies**: 100% local, CPU-compatible, zero token costs, sub-10ms response latency.
- **Comprehensive Automated Test Suite**: 146 automated tests with 100% pass rate covering configuration, dataset schema, tokenization, lemmatization, vectorization, edge cases, and full regression.

---

## 🏛️ Knowledge Base Domain & Categories

| Category | Topics Covered | Sample Queries |
| :--- | :--- | :--- |
| **Academic Registration & Records** | Course enrollment, add/drop periods, official transcripts, prerequisite waivers, degree audits. | *"How do I register for classes?"*, *"Where can I order my grades transcript?"* |
| **Tuition & Financial Services** | Payment channels, installment plans, late penalties, scholarships, refund schedules. | *"Where do I pay my tuition bill?"*, *"Can I pay in monthly installments?"* |
| **Campus ID & Physical Access** | New student IDs, lost card replacement, lab keycard access, semester parking permits. | *"Where can I get my student ID card?"*, *"How do I replace a lost card?"* |
| **Library & Academic Resources** | Book borrowing limits, group study rooms, remote proxy access, interlibrary loans. | *"How many books can I borrow?"*, *"Can I book a library study room?"* |
| **Campus IT & Technical Support** | eduroam Wi-Fi setup, password resets, free student software (Office 365, MATLAB), IT Helpdesk. | *"What is the Wi-Fi password?"*, *"Do students get free Microsoft Office?"* |

---

## 🛠️ Technology Stack

| Layer | Component | Description & Justification |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ (tested on 3.10 and 3.13) | Standard language for NLP engineering, clean, and portable. |
| **User Interface** | Streamlit | Reactive web frontend with cached models and zero frontend build overhead. |
| **NLP Pipeline** | NLTK | WordNet morphological lemmatization and English stop-words. |
| **Vector Space Model** | scikit-learn (`TfidfVectorizer`) | Unigram + bigram TF-IDF representations and inner-product Cosine Similarity. |
| **Array Computing** | NumPy | Vector dot products, similarity score ranking, and array operations. |
| **Testing** | pytest | Automated unit, integration, edge-case, and parameterized regression suites. |

---

## 🚀 Quickstart Guide

### 1. Clone & Navigate
```bash
git clone https://github.com/UdoySadik/codealpha_tasks.git
cd codealpha_tasks/Chatbot_for_FAQs_Task2
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Activate on Windows (cmd.exe):
.\venv\Scripts\activate.bat
# Activate on Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Offline NLTK Corpora (One-Time Setup)
```bash
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); print('NLTK corpora ready')"
```

### 5. Run the Automated Test Suite
```bash
pytest -v
```

### 6. Launch the Interactive Web Application
```bash
streamlit run app.py
```
Open your browser to the local URL (typically `http://localhost:8501`).

---

## 🧪 Automated Testing Verification

The project includes 7 dedicated automated test suites covering every layer of the architecture:

```text
tests/
├── test_config.py          # 6 tests: configuration defaults, environment overrides, immutability
├── test_knowledge_base.py  # 7 tests: JSON schema, duplicate ID checks, missing/corrupted file handling
├── test_preprocessor.py    # 6 tests: tokenization, stop-words, noun/verb lemmatization, idempotence
├── test_matcher.py         # 8 tests: TF-IDF vectorization, exact matches, threshold boundaries, fallback
├── test_app.py             # 3 tests: engine caching, Streamlit loader, end-to-end integration
├── test_edge_cases.py      # 6 tests: >1000 char queries, emojis, script/SQL injections, foreign languages
└── test_regression.py      # 110 tests: 100% parameterization across all 22 FAQs and 88 patterns
```

**Test Execution Outcome:**
```text
============================ 146 passed in 10.42s =============================
```

---

## 📁 Repository Structure

```text
Chatbot_for_FAQs_Task2/
├── .gitignore                  # Git exclusion rules
├── .env.example                # Local configuration template
├── README.md                   # Comprehensive project guide and documentation
├── architecture.md             # In-depth architectural design, data flows, and math
├── design.md                   # UI/UX specifications, colors, wireframes, WCAG rules
├── memory.md                   # Persistent project context and state tracking
├── prd.md                      # Product Requirements Document & Acceptance Criteria
├── task.md                     # Phased task checklist with unique IDs
├── implementation_plan.md      # Engineering execution roadmap and phase gates
├── DECISIONS.md                # Architecture Decision Records (ADRs)
│
├── .streamlit/
│   └── config.toml             # Deep Slate & Indigo theme configuration
│
├── data/
│   └── faqs.json               # Curated FAQ dataset (22 intents, 88 patterns)
│
├── src/
│   ├── __init__.py             # Core package namespace
│   ├── config.py               # Centralized configuration dataclass
│   ├── knowledge_base.py       # Knowledge base loader, validator, pattern indexer
│   ├── preprocessor.py         # NLTK tokenization, stop-words, WordNet lemmatizer
│   └── matcher.py              # TF-IDF vectorizer, coverage-weighted cosine similarity
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_knowledge_base.py
│   ├── test_preprocessor.py
│   ├── test_matcher.py
│   ├── test_app.py
│   ├── test_edge_cases.py
│   └── test_regression.py
│
├── app.py                      # Interactive Streamlit web application
└── requirements.txt            # Pinned dependencies
```

---

## 👥 Authors & Acknowledgments

- **Developer**: Md Farhan Sadik Udoy ([@UdoySadik](https://github.com/UdoySadik))
- **Program**: CodeAlpha Artificial Intelligence Internship
- **Task**: Task 2 — Chatbot for FAQs
