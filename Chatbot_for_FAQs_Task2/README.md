# 🤖 Intelligent FAQ Chatbot

> **CodeAlpha Artificial Intelligence Internship — Task Submission Project**  
> **Status:** Stage 0 — Documentation & Architecture Blueprint (Implementation Pending Approval)

---

## 📌 Project Overview

The **Intelligent FAQ Chatbot** is a lightweight, transparent, and deterministic Natural Language Processing (NLP) system designed to accept natural-language queries from users and retrieve the most relevant answer from a curated Knowledge Base.

Unlike simple keyword lookups, this system applies standard NLP text preprocessing, converts text into mathematical vector representations using **TF-IDF (Term Frequency-Inverse Document Frequency)**, and calculates vector proximity using **Cosine Similarity**. If a user's question fails to reach a configurable confidence threshold, the chatbot safely returns a polite, helpful fallback response instead of hallucinating or serving unrelated information.

---

## 🎯 Scope and Objectives

### Primary Objectives
- **Natural Language Understanding**: Preprocess raw user queries (lowercasing, punctuation stripping, tokenization, stop-word filtering, and lemmatization).
- **Mathematical Similarity Matching**: Construct a vector space model over FAQ question patterns using TF-IDF and identify nearest neighbors via Cosine Similarity.
- **Configurable Threshold Filtering**: Guarantee high precision by rejecting low-similarity matches via an adjustable cutoff threshold ($T \in [0.0, 1.0]$).
- **Polite Fallback Mechanism**: Gracefully handle queries outside the domain without misleading users.
- **Interactive Web Interface**: Provide a modern, intuitive, responsive chat experience built with Streamlit.
- **Automated Verification**: Deliver a comprehensive automated test suite with `pytest` covering edge cases, preprocessing rules, threshold boundaries, and regression testing.

---

## 🛠️ Proposed Technology Stack

| Layer | Technology | Justification |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Standard language for AI/NLP engineering, readable, and widely supported. |
| **User Interface** | Streamlit | Native chat primitives (`st.chat_message`, `st.chat_input`), rapid prototyping, clean reactive state management, zero frontend build overhead. |
| **NLP & Preprocessing** | NLTK (`nltk`) / Standard Library | Deterministic tokenization, stop-word removal, and WordNet lemmatization. Runs 100% offline. |
| **Vectorization & Math** | scikit-learn (`TfidfVectorizer`) | Production-tested, highly optimized TF-IDF matrix generation and cosine similarity calculation. |
| **Numerical Arrays** | NumPy | High-performance array operations for score ranking and threshold filtering. |
| **Automated Testing** | pytest | Industry-standard Python test framework for unit, integration, and edge-case verification. |
| **Data Format** | JSON (`faqs.json`) | Human-readable, structured, maintainable, supporting multiple question patterns per intent. |

---

## 🏛️ Proposed Knowledge Base Domain

**Recommended Domain**: **University Student Academic & Campus Services**  
- **Justification**: Rich lexical variety, highly realistic user queries (admissions, course registration, tuition payment, library access, grading policies, student IDs, IT support), and clearly definable category boundaries.
- **Safety & Factuality**: Answers reflect standard generic university administrative workflows. Specific illustrative items (e.g., sample office hours) are explicitly tagged as illustrative to avoid factual misrepresentation.
- **Alternative Evaluated**: CodeAlpha Internship Program FAQ (can be selected if the user prefers an internship-specific domain).

---

## 📋 System Setup Plan (For Implementation Phase)

Once Stage 0 documentation is approved, the project will follow this standard local setup:

```bash
# 1. Clone repository / Navigate to directory
cd "Chatbot for FAQs"

# 2. Create and activate a Python virtual environment
python -m venv venv

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (cmd.exe):
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# 3. Install approved dependencies
pip install -r requirements.txt

# 4. Download required NLTK corpora (punkt, stopwords, wordnet)
python -m nltk.downloader punkt stopwords wordnet

# 5. Run automated test suite
pytest -v

# 6. Launch the Streamlit application
streamlit run app.py
```

---

## 🚀 Application Usage Outline

1. **Start the Chatbot**: Launch via `streamlit run app.py` and open the local browser URL (typically `http://localhost:8501`).
2. **Review Suggested Prompts**: The landing state offers sample queries (e.g., *"How do I register for classes?"*, *"Where can I get my student ID card?"*).
3. **Ask Natural-Language Questions**: Type questions into the chat input bar at the bottom.
4. **Observe Matching Confidence**: The system displays the most relevant answer. When confidence display is enabled, the match score is shown for transparency.
5. **Fallback Handling**: If an out-of-domain query is asked (e.g., *"What is the weather in Tokyo?"*), the chatbot politely triggers the fallback response.
6. **Session Reset**: Users can clear the current conversation history using the sidebar control.

---

## 📁 Repository Structure Blueprint

```text
Chatbot for FAQs/
├── .gitignore               # Git exclusion rules
├── .env.example             # Local configuration template (no secrets)
├── README.md                # Project overview and instructions
├── architecture.md          # Technical design and data flow diagrams
├── design.md                # UI/UX specification and styling guidelines
├── memory.md                # Persistent project context and state tracking
├── prd.md                   # Product Requirements Document
├── task.md                  # Granular phased task checklist
├── implementation_plan.md   # Execution roadmap and verification gates
├── DECISIONS.md             # Architecture Decision Records (ADRs)
│
├── data/                    # Knowledge base directory (Phase 2)
│   └── faqs.json            # Curated FAQ dataset with question variants
│
├── src/                     # Core application source code (Phase 1+)
│   ├── __init__.py
│   ├── config.py            # Centralized settings & thresholds
│   ├── preprocessor.py      # NLP text normalization pipeline
│   ├── matcher.py           # TF-IDF vectorizer and cosine similarity engine
│   └── knowledge_base.py    # FAQ data loader and validation schema
│
├── tests/                   # Automated pytest suite (Phase 5)
│   ├── __init__.py
│   ├── test_preprocessor.py # Tokenizer and lemmatizer unit tests
│   ├── test_matcher.py      # TF-IDF, similarity score & fallback tests
│   └── test_knowledge_base.py # Schema & dataset integrity tests
│
├── app.py                   # Streamlit web application entry point (Phase 4)
└── requirements.txt         # Pinned production and test dependencies (Phase 1)
```

---

## 🚦 Current Development Status

- [x] **Stage 0**: Architecture, UI/UX Design, and Engineering Documentation complete.
- [ ] **Stage 0 Approval**: Awaiting user command `APPROVE DOCUMENTATION`.
- [ ] **Phase 1**: Project skeleton, configuration, and dependencies (PENDING).
- [ ] **Phase 2**: FAQ dataset and NLP preprocessing engine (PENDING).
- [ ] **Phase 3**: Vectorization, similarity matching, and threshold logic (PENDING).
- [ ] **Phase 4**: Streamlit Chat Interface and engine integration (PENDING).
- [ ] **Phase 5**: Automated testing suite & edge-case validation (PENDING).
- [ ] **Phase 6**: UI polish, accessibility, and documentation wrap-up (PENDING).
- [ ] **Phase 7**: GitHub readiness & final submission packaging (PENDING).
