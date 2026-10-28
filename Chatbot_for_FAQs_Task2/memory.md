# 🧠 Project Memory & Context — FAQ Chatbot

> **Role:** Persistent memory and execution state tracking.  
> **Last Updated:** Stage 0 Completion  
> **Next Authorized Action:** Await user command `APPROVE DOCUMENTATION`.

---

## 1. Project Context & Identity

- **Project Name**: Intelligent FAQ Chatbot for Student & Campus Services
- **Internship**: CodeAlpha Artificial Intelligence Internship
- **Current Stage**: **Stage 0 — Documentation & Architecture Blueprint**
- **Repository Location**: `c:\Users\Udoy\Desktop\Varsity\codealpha_tasks\Chatbot for FAQs`
- **Execution Mode**: Local-only, CPU-compatible, zero external paid API credentials.

---

## 2. Decision Status Summary

### 2.1 Proposed Decisions (Awaiting User Approval)
- **ADR-001 (Tech Stack)**: Python 3.10+, Streamlit, scikit-learn (TF-IDF + Cosine Similarity), NLTK (tokenization + WordNet lemmatization), pytest.
- **ADR-002 (Domain)**: University Student Academic & Campus Services (Admissions, Registration, Tuition & Finance, Campus ID, Academic Policies).
- **ADR-003 (Storage Format)**: `data/faqs.json` with multi-pattern array per intent.
- **ADR-004 (NLP Pipeline)**: Lowercasing, regex punctuation removal, tokenization, stop-word removal, and WordNet lemmatization.
- **ADR-005 (Vector Engine)**: `TfidfVectorizer(ngram_range=(1,2))` with Cosine Similarity.
- **ADR-006 (Threshold)**: Default similarity cutoff $\tau = 0.30$ with polite fallback messaging.
- **ADR-007 (UI)**: Streamlit interactive chat interface with suggested prompts, score inspection, and session reset.
- **ADR-008 (Testing)**: Automated pytest suites covering preprocessor, matcher, threshold edge cases, and regression.

### 2.2 Confirmed Decisions
- Strictly documentation-first workflow.
- Do not write application source code, install packages, or launch apps until documentation is explicitly approved.
- Sequential phase rollout: after every phase, execute tests, report actual results, update documentation, and wait for `CONTINUE`.

---

## 3. Phased Progress Tracking

| Phase | Description | Status | Verification Result |
| :--- | :--- | :--- | :--- |
| **Stage 0** | Blueprint, Architecture & Documentation | **COMPLETED (Awaiting Approval)** | All 9 blueprint files created & validated. |
| **Phase 1** | Project Setup & Skeleton | **PENDING** | Not started. |
| **Phase 2** | FAQ Dataset & NLP Preprocessing Engine | **PENDING** | Not started. |
| **Phase 3** | TF-IDF Vectorization & Similarity Engine | **PENDING** | Not started. |
| **Phase 4** | Streamlit Chat Interface & Integration | **PENDING** | Not started. |
| **Phase 5** | Automated Testing & Regression Suite | **PENDING** | Not started. |
| **Phase 6** | UI Polish & Documentation Update | **PENDING** | Not started. |
| **Phase 7** | GitHub Readiness & Submission | **PENDING** | Not started. |

---

## 4. Operational Constraints & Guardrails

1. **No Cloud LLM / No API Keys**: System must operate 100% deterministically and offline using local scikit-learn / NLTK.
2. **Modular Code Structure**: Separation of concerns (`src/config.py`, `src/knowledge_base.py`, `src/preprocessor.py`, `src/matcher.py`, `app.py`).
3. **Transparent Confidence Reporting**: Never present raw cosine similarity as a calibrated probability.
4. **Threshold Integrity**: Low-confidence or out-of-domain queries must cleanly return fallback text rather than misleading answers.
5. **No Code Without Approval**: Do not advance to Phase 1 until the user explicitly responds with `APPROVE DOCUMENTATION`.

---

## 5. Known Issues & Risks

- **Issue / Risk 1**: NLTK corporate network download issues during corporate or offline setups.
  - *Mitigation*: Design lazy bootstrap with fallbacks and pre-download instructions in `README.md`.
- **Issue / Risk 2**: Streamlit script re-execution latency on vectorizer fitting.
  - *Mitigation*: Use `@st.cache_resource` for the vectorizer and knowledge base instance.

---

## 6. Next Authorized Action

**AWAIT EXPLICIT USER COMMAND:**
> `APPROVE DOCUMENTATION`

*(Do NOT run tests, install packages, or write Python application code until this command is received.)*
