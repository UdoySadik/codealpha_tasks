# 📄 Product Requirements Document (PRD) — FAQ Chatbot

> **Project:** CodeAlpha AI Internship — FAQ Chatbot  
> **Status:** Stage 0 Blueprint (Pending Approval)  
> **Target Version:** MVP 1.0.0  

---

## 1. Problem Statement

Students, interns, and campus community members frequently need answers to routine questions regarding academic policies, course registrations, tuition fees, library access, and campus services. In typical institutions, these queries are buried across lengthy PDF handbooks or fragmented web pages, leading to repetitive support tickets and delayed assistance.

A rigid keyword-matching search frequently fails when users phrase questions using natural language, synonyms, or paraphrasing (e.g., *"How much is the cost per credit?"* vs. *"Tuition fee schedule"*). Conversely, unconstrained generative AI models often hallucinate policies or require paid API tokens.

There is a direct need for an **accurate, deterministic, local, and zero-cost FAQ Chatbot** that bridges natural language variation through mathematical vector similarity while enforcing strict threshold boundaries to prevent false information.

---

## 2. Target Users & Personas

1. **Undergraduate / Graduate Student (Primary User)**:
   - Needs fast, reliable answers to administrative procedures (e.g., how to drop a class, pay tuition, or obtain an ID).
   - Phrases queries informally and expects immediate answers.
2. **Academic Advisor / Support Desk Staff**:
   - Benefits from the chatbot deflecting common Tier-1 questions.
   - Evaluates system transparency and accuracy.
3. **Internship Evaluator (CodeAlpha Reviewer)**:
   - Assesses NLP engineering methodology, code modularity, preprocessing rigor, mathematical vectorization, testing coverage, and architectural documentation.

---

## 3. Product Goals & Objectives

- **G-1**: Deliver sub-second query retrieval locally without external network or API dependencies.
- **G-2**: Achieve reliable question intent recognition using TF-IDF vectorization and Cosine Similarity.
- **G-3**: Enforce a strict confidence threshold ($\tau = 0.30$) preventing false-positive matches for out-of-domain queries.
- **G-4**: Provide an accessible, responsive, and visually appealing web interface using Streamlit.
- **G-5**: Ensure 100% reproducible execution and automated test coverage across all pipeline stages.

---

## 4. Functional Requirements (FR)

### 4.1 Knowledge Base & Data Management
- **FR-1.1**: The knowledge base MUST be stored separately from code in a clean, human-readable format (`data/faqs.json`).
- **FR-1.2**: Each FAQ record MUST include a unique ID (`id`), category (`category`), canonical question (`question`), a list of paraphrased question patterns (`patterns`), a verified answer (`answer`), and an illustrative status flag (`verified: true/false`).
- **FR-1.3**: The knowledge base MUST cover at least 5 primary student services categories with at least 20 curated FAQ items and 3+ question variations per item to allow robust testing.
- **FR-1.4**: Non-verified illustrative answers MUST be clearly flagged to prevent factual misrepresentation.

### 4.2 NLP Preprocessing Pipeline
- **FR-2.1**: The system MUST normalize incoming text to lowercase.
- **FR-2.2**: The system MUST strip punctuation and non-alphanumeric noise while preserving meaningful tokens and numeric identifiers.
- **FR-2.3**: The system MUST tokenize text into discrete word tokens.
- **FR-2.4**: The system MUST filter common English stop-words using a standard stop-word lexicon (NLTK) without stripping critical intent tokens.
- **FR-2.5**: The system MUST lemmatize tokens to base morphological forms using NLTK WordNet lemmatizer.
- **FR-2.6**: Preprocessing MUST be deterministic and idempotent.

### 4.3 Vector Representation & Matching Engine
- **FR-3.1**: The system MUST fit a `TfidfVectorizer` (with unigrams and bigrams, e.g., `ngram_range=(1,2)`) across all preprocessed FAQ pattern variations.
- **FR-3.2**: Incoming user queries MUST be transformed into the identical TF-IDF vector space.
- **FR-3.3**: Cosine similarity MUST be calculated between the query vector and all indexed pattern vectors.
- **FR-3.4**: The system MUST select the highest-scoring candidate FAQ item ($S_{max}$).
- **FR-3.5**: If $S_{max} \ge \tau$ (default 0.30), the system MUST return the matched FAQ answer.
- **FR-3.6**: If $S_{max} < \tau$, the system MUST return the polite fallback response.
- **FR-3.7**: Empty or whitespace-only queries MUST NOT be passed to the vectorizer; they MUST return an explicit empty-input warning.

### 4.4 User Interface & Interaction
- **FR-4.1**: The UI MUST provide a conversational chat timeline with clear visual distinctions between user and bot messages.
- **FR-4.2**: The UI MUST support a sticky chat input at the bottom of the window.
- **FR-4.3**: When conversation history is empty, the UI MUST display welcoming guidance and clickable suggestion chips.
- **FR-4.4**: The UI MUST provide a sidebar displaying knowledge base metrics (total FAQs, categories).
- **FR-4.5**: The UI MUST provide a "Clear Chat" button to reset the session.
- **FR-4.6**: The UI MUST allow toggling confidence score visibility in the sidebar.

---

## 5. Non-Functional Requirements (NFR)

- **NFR-1 (Performance)**: End-to-end query processing and response rendering MUST complete in $< 100\text{ ms}$ on standard modern hardware.
- **NFR-2 (Local Execution & Cost)**: The system MUST run 100% locally on standard CPU hardware with zero external API fees or internet reliance after package installation.
- **NFR-3 (Code Quality & Modularity)**: Application code MUST adhere strictly to PEP 8 standards with modular segregation across `config`, `knowledge_base`, `preprocessor`, `matcher`, and `app`.
- **NFR-4 (Testability)**: All core components (preprocessor, vectorizer, matcher, schema validation) MUST be verified via automated `pytest` test suites.
- **NFR-5 (Accessibility)**: The UI MUST meet WCAG 2.1 AA contrast standards ($> 4.5:1$) and support standard keyboard navigation.

---

## 6. User Stories & Acceptance Criteria

### User Story 1: Paraphrased Query Retrieval
> *As a student, I want to ask "Where do I pay my semester fees?" so that I can find the tuition payment process even if the official question is written as "How can tuition fees be settled?"*
- **Acceptance Criteria**: Preprocessor normalizes both phrases to core stems (`pay`, `semester`, `fee`, `tuition`); matcher calculates cosine similarity above threshold $\tau = 0.30$; expected tuition answer is returned.

### User Story 2: Out-of-Domain Fallback Protection
> *As a user, when I ask an irrelevant question like "What is the capital of France?", I want the chatbot to acknowledge that it cannot answer rather than giving me a misleading campus answer.*
- **Acceptance Criteria**: Query vectors share zero vocabulary with the campus FAQ database; calculated similarity is $< 0.30$; system returns `FALLBACK_MESSAGE`.

### User Story 3: Empty Query Safeguard
> *As a user, if I accidentally hit submit with only spaces, I want immediate guidance without breaking the application.*
- **Acceptance Criteria**: Input length check detects empty string; application does not crash; warns user to enter a question.

### User Story 4: Transparent Confidence Inspection
> *As an evaluator or administrator, I want to inspect the cosine similarity score for a given match so that I can calibrate the threshold effectively.*
- **Acceptance Criteria**: Toggling "Show Confidence Score" displays the raw cosine similarity score (e.g., `0.78`) underneath the assistant's answer.

---

## 7. Scope Definition

### In Scope (MVP 1.0.0)
- Curated JSON dataset for Campus Services with 20+ Q&As and 60+ question variants.
- NLTK-based normalization and lemmatization pipeline.
- Scikit-learn TF-IDF vectorization with Cosine Similarity matching.
- Configurable threshold filtering with polite fallback.
- Streamlit interactive web interface with suggestion chips, clear chat, and score inspector.
- Comprehensive automated pytest suite covering all modules and edge cases.

### Out of Scope (Explicitly Deferred)
- User authentication and login accounts.
- Persistent external database (PostgreSQL, MongoDB).
- Cloud deployment and remote hosting infrastructure.
- Generative LLM APIs (OpenAI, Anthropic, Gemini API) — zero paid credentials requirement.
- Voice-to-text / speech recognition input.

---

## 8. Definition of Done (DoD)

A phase or feature is considered **Done** only when:
1. Architectural and design documentation is updated and accurate.
2. Code is cleanly written, commented, and adheres to modular boundaries.
3. Automated unit and integration tests are written and execute with a 100% `PASS` rate.
4. Edge cases (empty string, out-of-domain query, missing data file) are explicitly handled.
5. No regressions are introduced to previous functionality.
6. The user explicitly reviews and issues the `CONTINUE` command.
