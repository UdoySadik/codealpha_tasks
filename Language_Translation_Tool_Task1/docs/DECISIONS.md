# Architecture Decision Records (ADR) Log
## Project: Language Translation Tool (Task 1)
**Program:** CodeAlpha Artificial Intelligence Internship  
**Document Status:** Approved (Stage 0 Complete)  
**Author:** Lead Architect  
**Last Updated:** 2026-10-27  

---

## Decision Status Legend
- **PROPOSED**: Suggested technical decision undergoing user/mentor review in Stage 0.
- **APPROVED**: Formally authorized by the project lead / user.
- **REJECTED**: Evaluated and discarded in favor of an alternative.
- **SUPERSEDED**: Replaced by a subsequent decision record.

---

## ADR-001: System Architecture Pattern (Single-Process Server + Modern Web SPA)

- **Status**: `APPROVED`
- **Context**: The project requires building a user-friendly, responsive Language Translation Tool in Python for the CodeAlpha AI Internship. We must decide whether to build a multi-process architecture (separate Node.js frontend + separate Python backend), a Streamlit application, or a unified single-process Python web server that directly serves a modern Vanilla Web Single Page Application (SPA).
- **Alternatives Considered**:
  1. *Streamlit Single-Script App*: Very fast to implement, but severely restricts custom glassmorphic styling, requires awkward hacks for smooth clipboard tooltips, and limits fine-grained control over browser Web Speech audio APIs.
  2. *Dual-Server Setup (Vite React Frontend + FastAPI Backend)*: Requires both Python and Node.js/npm environments, introduces cross-origin CORS complexity, and creates installation friction for evaluators who only want to clone and run.
  3. *Unified Python Web Server + Vanilla HTML5/CSS3/ES6 Frontend*: Python web server handles API routing, secret management, and static file serving in one lightweight command (`python app.py`). The frontend is high-performance, requires zero npm build steps, and allows 100% control over design aesthetics.
- **Decision**: Adopt Alternative 3 (Unified Python Server + Vanilla HTML5/CSS3/ES6 Frontend).
- **Consequences**:
  - *Positive*: Zero node/npm dependencies, single command startup, 100% aesthetic freedom, easy local testing, minimal footprint.
  - *Negative*: Handcrafted DOM updates in ES6 JavaScript instead of React component state, but since the UI consists of two primary panels, Vanilla JS is lightweight, reliable, and clean.

---

## ADR-002: Pluggable Translation Provider Architecture & Explicit Dev Fallback

- **Status**: `APPROVED`
- **Context**: The project requires integrating with a real translation API (such as Google Cloud Translation API or Microsoft Azure Translator). However, student interns and reviewers often do not possess a paid or active cloud billing account with active credit cards. We must guarantee that the system can work seamlessly with real cloud APIs when keys are present, but also provide an explicitly labeled, functional development fallback mode when credentials are absent, without ever disguising mock responses as real API translations.
- **Alternatives Considered**:
  1. *Hardcoded Single Provider (e.g. Google Cloud only)*: If the user lacks a GCP key, the entire application fails to function.
  2. *Unofficial Web Scraping Library (e.g. `googletrans`)*: Frequently breaks without warning, violates service terms, and returns HTTP 429 / 403 errors unpredictably.
  3. *Provider Interface Pattern with Configurable Adapters*: Create an abstract `TranslationProvider` base class with concrete implementations for Google Cloud, Azure Translator, DeepL, MyMemory (free public API), and a local `DevEchoFallbackProvider`.
- **Decision**: Adopt Alternative 3. The server inspects the `.env` configuration file. If `TRANSLATION_PROVIDER=google`, `azure`, `deepl`, or `mymemory` is set with valid credentials, it dispatches to that cloud API. If set to `dev_fallback` or if no keys are provided, it engages the explicit dev fallback and signals `is_fallback: true` in the API payload, which triggers a prominent, honest warning badge in the UI.
- **Consequences**:
  - *Positive*: 100% compliance with strict internship requirements (no faking real API calls; graceful fallback; no crashes if keys are missing). Pluggable and enterprise-ready.
  - *Negative*: Requires writing adapter classes for each provider, which is easily managed within the modular architecture.

---

## ADR-003: Backend Micro-Framework Selection (Flask vs. FastAPI)

- **Status**: `APPROVED`
- **Context**: We need to choose the Python backend framework to serve the API and static files.
- **Alternatives Considered**:
  1. *FastAPI + Uvicorn*: Excellent async performance, automatic OpenAPI docs, and Pydantic validation. However, requires multiple extra packages (`fastapi`, `uvicorn`, `pydantic`).
  2. *Flask*: Included in standard Python web curriculum, mature, lightweight, minimal dependencies (`flask`, `requests`, `python-dotenv`), synchronous request-response flow is straightforward to understand and test, and static asset serving is built-in.
  3. *Django*: Massive overengineering for a single-page translation utility.
- **Decision**: Recommend **Flask** for its simplicity, standard library feel, zero async overhead, and minimal dependency footprint. (FastAPI remains an acceptable alternative if async concurrency is specifically requested by the user).
- **Consequences**:
  - *Positive*: Simple installation, minimal lines of boilerplate, highly readable code for academic/internship review.
  - *Negative*: Synchronous request handling by default; mitigated because translation requests are I/O bound with small payloads and fast response times.

---

## ADR-004: Frontend Styling & Design System (Vanilla CSS with Design Tokens)

- **Status**: `APPROVED`
- **Context**: The user and system instructions emphasize high visual aesthetics ("wow factor", glassmorphism, dark/light modes, micro-animations) while avoiding TailwindCSS unless explicitly requested.
- **Alternatives Considered**:
  1. *Bootstrap / Tailwind via CDN*: Bulky, opinionated, often looks generic, introduces external network dependencies.
  2. *Hand-crafted Vanilla CSS3 with Custom Properties (Variables)*: Full design autonomy, zero external dependencies, native support for CSS variables, smooth hardware-accelerated transitions, and custom backdrop-filter glassmorphism.
- **Decision**: Adopt pure Vanilla CSS (`style.css`) using curated HSL/Hex design tokens, modern typography via Google Fonts (Inter & Outfit), and responsive flex/grid layouts.
- **Consequences**:
  - *Positive*: Stunning, unique, customized aesthetic; lightweight; complete control over animations and themes.
  - *Negative*: Requires intentional writing of CSS rules, which is fully accounted for in the design specifications.

---

## ADR-005: Security, Secret Management & Server Proxying

- **Status**: `APPROVED`
- **Context**: Cloud translation APIs require confidential API keys or service account credentials. These must never be exposed to the client browser or committed to version control.
- **Alternatives Considered**:
  1. *Direct Browser-to-Cloud Calling*: Client JavaScript holds API keys and calls Google/Azure directly. Critical security vulnerability (keys are visible in DevTools Network tab and page source).
  2. *Server-Side Proxy with `.env`*: Frontend calls backend `/api/translate`; backend securely loads keys from `.env` using `python-dotenv` and calls upstream cloud API.
- **Decision**: Strictly enforce Alternative 2. No client-side secret exposure under any circumstances. `.env` is listed in `.gitignore`. A sanitized `.env.example` is maintained.
- **Consequences**:
  - *Positive*: Zero security risk; prevents API quota theft; centralizes input sanitization and rate limiting.
  - *Negative*: None. This is standard industry best practice.

---

## ADR-006: Text-to-Speech (TTS) Strategy

- **Status**: `APPROVED`
- **Context**: An approved optional feature is audio pronunciation of source and translated text.
- **Alternatives Considered**:
  1. *Backend TTS (e.g. gTTS or Google Cloud Text-to-Speech API)*: Generates audio files on the server and streams them as MP3. Adds significant network latency, disk I/O, and consumes extra API quotas.
  2. *Native Browser Web Speech API (`window.speechSynthesis`)*: Built directly into modern browsers (Chrome, Edge, Firefox, Safari); zero server load; zero latency; native multilingual voice support.
- **Decision**: Adopt the native **Web Speech API** on the client side.
- **Consequences**:
  - *Positive*: Zero backend overhead, instant audio playback, works offline, supports dozens of voices natively.
  - *Negative*: Voice quality depends on the user's operating system and browser voices; handles graceful degradation if the browser lacks a specific language voice.
