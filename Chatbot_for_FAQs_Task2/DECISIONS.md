# 📜 Architecture Decision Records (ADR) — FAQ Chatbot

> **Document Status:** All decisions below are **PROPOSED** for user review and approval in Stage 0.  
> Once approved via the `APPROVE DOCUMENTATION` command, their status will transition to **APPROVED**.

---

## Decision Index

- [ADR-001: Technology Stack Selection](#adr-001-technology-stack-selection)
- [ADR-002: FAQ Knowledge Base Domain Selection](#adr-002-faq-knowledge-base-domain-selection)
- [ADR-003: Knowledge Base Storage Format & Schema](#adr-003-knowledge-base-storage-format--schema)
- [ADR-004: NLP Preprocessing & Lemmatization Pipeline](#adr-004-nlp-preprocessing--lemmatization-pipeline)
- [ADR-005: Vector Representation & Similarity Metric](#adr-005-vector-representation--similarity-metric)
- [ADR-006: Similarity Threshold & Fallback Policy](#adr-006-similarity-threshold--fallback-policy)
- [ADR-007: Presentation Layer (Streamlit Framework)](#adr-007-presentation-layer-streamlit-framework)
- [ADR-008: Automated Testing Framework & Quality Gates](#adr-008-automated-testing-framework--quality-gates)

---

## ADR-001: Technology Stack Selection

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
The project requires building a functional, maintainable, transparent NLP FAQ chatbot for the CodeAlpha Artificial Intelligence Internship. The solution must run 100% locally on standard developer hardware without paid API keys, cloud subscriptions, or complex infrastructure.

### Considered Options:
1. **Python + Streamlit + scikit-learn + NLTK + pytest (Recommended)**: Minimal footprint, native chat widgets, robust information retrieval vectorizer, zero-latency local execution.
2. **FastAPI + React/Next.js**: Higher development complexity, requires managing two runtime processes, frontend build pipelines, and unnecessary overhead for a single-purpose FAQ chatbot.
3. **LangChain / LlamaIndex + Local LLM (Ollama)**: Heavy compute requirements (8GB+ VRAM/RAM), non-deterministic responses, hallucination risks, sluggish query response on standard laptops.

### Decision:
Adopt **Option 1**: Python 3.10+, Streamlit for the user interface, scikit-learn for TF-IDF and Cosine Similarity, NLTK for preprocessing and lemmatization, and pytest for automated testing.

### Consequences:
- **Pros**: Instant startup, clean maintainable code, zero API costs, deterministic testing, perfectly tailored to CodeAlpha internship evaluation criteria.
- **Cons**: Limited to TF-IDF semantic capture (handled via multi-pattern FAQ variants).

---

## ADR-002: FAQ Knowledge Base Domain Selection

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
The project prompt requires selecting a clearly scoped domain with realistic questions and verified answers, avoiding invented facts or policies. We evaluated multiple candidates:
1. **University Student Academic & Campus Services (Recommended)**: Admissions, course registration, tuition payment, grading policy, campus IT, library access, student ID cards.
2. **CodeAlpha Internship Guidelines FAQ**: Internship duration, tasks, evaluation, submission requirements.
3. **E-commerce Customer Support FAQ**: Order tracking, returns, shipping, refunds.

### Decision:
Propose **Option 1: University Student Academic & Campus Services**.
- **Reasoning**: It provides an ideal domain with rich lexical variety, realistic natural-language paraphrasing, clear category boundaries, and high utility for students. Generic academic workflows are publicly verifiable. Illustrative answers (e.g., sample office hours) will be explicitly labeled as illustrative.

### Consequences:
- High natural language variation allows rigorous testing of TF-IDF and lemmatization.
- Easily extensible if the user later wishes to substitute an alternate domain.

---

## ADR-003: Knowledge Base Storage Format & Schema

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
FAQ questions and answers must be stored separately from matching and application logic in a maintainable, structured format.

### Considered Options:
1. **JSON (`data/faqs.json`) (Recommended)**: Native support for nested structures (such as a list of question pattern variations per FAQ intent), human-readable, schema-validatable.
2. **CSV (`data/faqs.csv`)**: Relational/tabular format, but clunky for storing multi-valued arrays of question patterns without custom delimiters.
3. **SQLite / Relational Database**: Adds unnecessary database migration overhead for a static, curated FAQ corpus of ~25-50 items.

### Decision:
Store the FAQ dataset in **`data/faqs.json`** using a structured schema:
```json
[
  {
    "id": "faq_acad_01",
    "category": "Academic Services",
    "question": "How do I register for semester courses?",
    "patterns": [
      "How do I enroll in classes for next semester?",
      "Where is the course registration portal?",
      "Can I add or drop a class online?",
      "Steps for enrolling in courses"
    ],
    "answer": "Course registration is completed online via the Student Academic Portal under 'Course Registration'. Select your semester, choose your approved courses, and click 'Confirm Registration'.",
    "verified": true
  }
]
```

### Consequences:
- Allows indexing multiple question variations per intent, drastically improving TF-IDF recall without duplicating answers.
- Simple to inspect, validate, and edit.

---

## ADR-004: NLP Preprocessing & Lemmatization Pipeline

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
Natural-language user queries exhibit varied word forms (e.g., "registered", "registering", "registration"). Text must be sanitized and normalized before vectorization.

### Considered Options:
1. **NLTK Regex Tokenizer + WordNet Lemmatizer + Stopwords (Recommended)**: Industry standard, lightweight, highly readable, supports morphological lemmatization.
2. **spaCy (`en_core_web_sm`)**: Powerful but introduces large binary model dependencies (~50MB download) and longer initialization times.
3. **Pure String Splitting + RegEx without Lemmatization**: Fails to unify inflected forms like "fees" and "fee" or "pay" and "paying".

### Decision:
Adopt **NLTK-based normalization**:
1. Case-folding (lowercasing).
2. Punctuation removal via regular expressions.
3. Word tokenization.
4. Stop-word filtering using `nltk.corpus.stopwords.words('english')`.
5. Morphological lemmatization using `nltk.stem.WordNetLemmatizer`.

### Consequences:
- Requires a one-time download of NLTK corpora (`punkt`, `stopwords`, `wordnet`).
- Produces normalized lemma strings optimized for TF-IDF vocabulary matching.

---

## ADR-005: Vector Representation & Similarity Metric

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
We must convert text documents into numerical representations and calculate similarity to retrieve the most relevant answer.

### Considered Options:
1. **`scikit-learn` `TfidfVectorizer` (unigrams + bigrams) + Cosine Similarity (Recommended)**:
   - High precision on keyword-dense domain FAQs.
   - Extremely fast computation ($< 5\text{ ms}$).
   - Fully transparent and testable mathematics.
2. **Dense Word Embeddings (Word2Vec / GloVe)**:
   - Requires pooling word vectors (e.g., mean pooling), which often dilutes domain-specific term significance.
3. **Exact String Jaccard / Levenshtein Distance**:
   - Ineffective for queries with different word order or syntactic variation.

### Decision:
Use **`scikit-learn.feature_extraction.text.TfidfVectorizer`** with `ngram_range=(1,2)` and `norm='l2'`, followed by **`scikit-learn.metrics.pairwise.cosine_similarity`**.

### Consequences:
- Bigram support captures two-word phrases like "id card", "tuition fee", "drop class".
- Cosine similarity values fall strictly in the interval $[0.0, 1.0]$.

---

## ADR-006: Similarity Threshold & Fallback Policy

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
When users ask out-of-domain questions (e.g., "How do I bake a cake?"), a pure nearest-neighbor lookup will still find the "closest" FAQ, even if it is completely irrelevant.

### Considered Options:
1. **Configurable Threshold ($\tau = 0.30$) with Fallback (Recommended)**:
   - Reject matches with $S_{max} < \tau$.
   - Return a polite fallback message with guidance.
2. **Always Return Top-1 Match**:
   - Results in unacceptable hallucinations and user confusion on irrelevant queries.
3. **Hardcoded High Threshold ($\tau = 0.70$)**:
   - Overly restrictive; rejects valid paraphrased queries.

### Decision:
Establish a default threshold **$\tau = 0.30$** (configurable via `config.py` and environment variable `SIMILARITY_THRESHOLD`). If the maximum cosine similarity score $S_{max} < \tau$, trigger the default fallback message:
> *"I'm sorry, but I couldn't find a sufficiently relevant answer in the FAQ database for your question. Could you please rephrase or reach out to student support?"*

### Consequences:
- High precision: avoids serving wrong answers.
- Threshold can be inspected and calibrated via the UI sidebar.

---

## ADR-007: Presentation Layer (Streamlit Framework)

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
The chatbot requires a user-friendly, responsive chat interface that displays conversation history, status banners, suggested prompts, and administrative metadata.

### Considered Options:
1. **Streamlit (Recommended)**:
   - Built-in `st.chat_message` and `st.chat_input` widgets.
   - Python-only stack, zero HTML/JS build complications.
   - Instant live reload and intuitive state management via `st.session_state`.
2. **CLI Terminal Interface**:
   - Functional for testing, but poor user experience and fails the visual excellence requirement.
3. **Custom Flask / FastAPI + HTML/CSS Web UI**:
   - Adds boilerplate routing, template rendering, and WebSocket/AJAX handling without substantial benefit.

### Decision:
Implement the interactive user interface using **Streamlit**.

### Consequences:
- Rapid development and clean UI.
- Direct integration with core Python NLP modules without REST API serialization overhead.

---

## ADR-008: Automated Testing Framework & Quality Gates

### Status: **PROPOSED** (Awaiting Stage 0 Approval)

### Context:
Strict engineering standards require automated testing at every phase covering exact matches, paraphrasing, empty inputs, out-of-domain rejection, and threshold boundaries.

### Considered Options:
1. **`pytest` Test Suite (Recommended)**:
   - Standard, expressive, fixtures, parameterized testing, clear diff reporting.
2. **`unittest` Standard Library**:
   - Verbose class-based boilerplate, less flexible parameterized tests.

### Decision:
Adopt **`pytest`** with test suites divided into:
- `test_preprocessor.py`: Unit tests for tokenization, lemmatization, edge cases.
- `test_knowledge_base.py`: Schema validation, loading integrity, missing file handling.
- `test_matcher.py`: TF-IDF matrix generation, exact match, paraphrased match, threshold boundary testing, out-of-domain rejection.

### Consequences:
- Guarantees 100% reproducible verification before phase progression.
