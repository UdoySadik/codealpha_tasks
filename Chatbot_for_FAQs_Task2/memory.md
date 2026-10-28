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

### 2.1 Approved Decisions
- **ADR-001 (Tech Stack)**: Python 3.10+, Streamlit, scikit-learn (TF-IDF + Cosine Similarity), NLTK (tokenization + WordNet lemmatization), pytest. (APPROVED)
- **ADR-002 (Domain)**: University Student Academic & Campus Services. (APPROVED)
- **ADR-003 (Storage Format)**: `data/faqs.json` with multi-pattern array per intent. (APPROVED)
- **ADR-004 (NLP Pipeline)**: Lowercasing, regex punctuation removal, tokenization, stop-word removal, and WordNet lemmatization. (APPROVED)
- **ADR-005 (Vector Engine)**: `TfidfVectorizer(ngram_range=(1,2))` with Cosine Similarity. (APPROVED)
- **ADR-006 (Threshold)**: Default similarity cutoff $\tau = 0.30$ with polite fallback messaging. (APPROVED)
- **ADR-007 (UI)**: Streamlit interactive chat interface with suggested prompts, score inspection, and session reset. (APPROVED)
- **ADR-008 (Testing)**: Automated pytest suites covering preprocessor, matcher, threshold edge cases, and regression. (APPROVED)

### 2.2 Workflow Governance
- Strictly documentation-first, phase-by-phase approval workflow.
- After every completed implementation phase, execute tests, report actual results, update documentation, and STOP.
- Await explicit user command `CONTINUE` before executing the next phase.

---

## 3. Phased Progress Tracking

| Phase | Description | Status | Verification Result |
| :--- | :--- | :--- | :--- |
| **Stage 0** | Blueprint, Architecture & Documentation | **COMPLETED** | All 10 blueprint files created and explicitly approved. |
| **Phase 1** | Project Setup & Skeleton | **COMPLETED** | `requirements.txt` installed; `src/`, `data/`, `tests/` structured; `src/config.py` implemented; 6/6 tests PASSED in 0.13s. |
| **Phase 2** | FAQ Dataset & NLP Preprocessing Engine | **COMPLETED** | `data/faqs.json` (22 FAQs, 5 cats, 88 patterns); `knowledge_base.py` & `preprocessor.py` implemented; 13/13 tests (19 total) PASSED in 6.36s. |
| **Phase 3** | TF-IDF Vectorization & Similarity Engine | **COMPLETED** | `src/matcher.py` implemented with TF-IDF, coverage-weighted cosine similarity, threshold & fallback; 8/8 tests (27 total) PASSED in 9.09s. |
| **Phase 4** | Streamlit Chat Interface & Integration | **COMPLETED** | `app.py` created with responsive Deep Slate/Indigo layout, suggestion chips, metadata badges, sidebar controls; headless server verified; 30/30 tests PASSED in 9.59s. |
| **Phase 5** | Automated Testing & Regression Suite | **COMPLETED** | Edge cases (emojis, long queries, injections, foreign languages) & 100% dataset regression (22 canonical + 88 patterns); 146/146 tests PASSED in 10.42s. |
| **Phase 6** | UI Polish & Documentation Update | **COMPLETED** | WCAG 2.1 AA focus visible outlines, responsive styling refined, README.md updated with test badges and setup instructions. |
| **Phase 7** | GitHub Readiness & Submission | **COMPLETED** | Zero secret leaks, `.gitignore` audit, PEP 8 compliance, `SUBMISSION_CHECKLIST.md` authored; 100% of tasks completed. |

---

## 4. Operational Constraints & Guardrails

1. **No Cloud LLM / No API Keys**: System operates 100% deterministically and offline using local scikit-learn / NLTK.
2. **Modular Code Structure**: Separation of concerns (`src/config.py`, `src/knowledge_base.py`, `src/preprocessor.py`, `src/matcher.py`, `app.py`).
3. **Transparent Confidence Reporting**: Never present raw cosine similarity as a calibrated probability.
4. **Threshold Integrity**: Low-confidence or out-of-domain queries must cleanly return fallback text rather than misleading answers.
5. **No Unauthorized Commits**: Maintain git hygiene without committing or pushing without explicit user instruction.

---

## 5. Known Issues & Risks

- **All Identified Risks Successfully Mitigated**:
  - NLTK corpora downloaded and cached locally for offline execution.
  - Streamlit model initialization cached via `@st.cache_resource` for sub-10ms response latency.
  - In-vocabulary coverage weighting prevents false positives on out-of-domain questions with incidental single-word overlaps.

---

## 6. Project Status & Next Action

**PROJECT FULLY COMPLETE & VERIFIED**
- All 10 required features + 5 optional features implemented.
- 146/146 automated tests passing deterministically.
- Awaiting final user review or git commit/push instructions.
