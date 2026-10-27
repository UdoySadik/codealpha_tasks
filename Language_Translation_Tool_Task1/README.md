# PolyGlot AI — Language Translation Tool
### Task 1 | CodeAlpha Artificial Intelligence Internship

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete%20%7C%20Verified-brightgreen.svg)](#development-status)
[![Tests](https://img.shields.io/badge/Tests-35%20Passed-brightgreen.svg)](#testing)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Interface](https://img.shields.io/badge/UI-Neo--Glassmorphic%20SPA-purple.svg)](#uiux-design)

---

## 1. Project Overview

**PolyGlot AI** is an enterprise-grade, clean, responsive, and secure **Language Translation Tool** engineered for the **CodeAlpha Artificial Intelligence Internship**.

The application decouples presentation from credential management using a **Single-Process Lightweight Server Architecture**. A Python Flask backend securely isolates cloud API keys and proxies requests through a **Pluggable Provider Adapter Layer**, while a modern Neo-Glassmorphic Single Page Application delivers a high-performance, accessible, and responsive user experience without heavy build steps.

> **Project Status:** All 7 phases are **100% complete, verified, and tested** with 35 automated tests passing with zero errors. The application runs immediately out of the box with zero external configuration required.

---

## 2. Features

### Core Requirements
- **Responsive Text Input**: Multi-line textarea supporting up to 5,000 Unicode characters with real-time character counting.
- **Source Language Detection**: Selection of 32 major international languages plus an intelligent `Auto-Detect` option.
- **Target Language Selection**: Alphabetically organized, searchable language picker covering major global languages.
- **Translate Action & Shortcuts**: Execute translation via primary action CTA or `Ctrl + Enter` (or `Cmd + Enter`).
- **Pluggable Translation Providers**:
  - `dev_fallback`: Built-in local offline engine with explicit fallback badging.
  - `mymemory`: Free public REST API client by Translated.net (no paid key required).
  - `google`: Google Cloud Translation API v2 adapter.
  - `azure`: Microsoft Azure Cognitive Services Translator v3.0 adapter.
  - `deepl`: DeepL REST API v2 adapter.
- **Honest System Transparency**: When running in development fallback mode, output is explicitly badged as `Development Fallback Mode`—mock responses are never disguised as real API translations.
- **State Indicators & Non-Blocking Spinners**: Animated loading spinner and disabled submit state during pending requests.
- **Robust Error Handling**: Contextual, user-friendly alert banners for empty input, upstream rate limits, and network dropouts.

### Approved Optional Usability Enhancements
- **One-Click Clipboard Copy**: Copies translated output with an animated `"Copied!"` visual confirmation.
- **Bidirectional Language Swap (`⇄`)**: Inverts source and target languages and transposes textarea text contents with 180° rotation micro-animation.
- **Multilingual Text-to-Speech (TTS)**: Native browser speech synthesis (`window.speechSynthesis`) with voice preloading and audio pulse animation.
- **Live Character Counter**: Dynamic visual indicator (`X / 5000 characters`) with amber (4,500) and red (5,000) threshold warnings.
- **Clear Action**: One-click reset for textareas, character counter, and status banners.
- **Dark & Light Mode**: Fluid theme toggle with persistent user preference stored in `localStorage`.
- **Collapsible Translation History**: In-session drawer storing the last 10 translations with individual item deletion, one-click restoration, and complete session clearing.

---

## 3. Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend Service** | Python 3.13 + Flask | Minimalist, robust, standard library feel, serves both API routes and static frontend assets in one lightweight command. |
| **Frontend UI** | Modern Vanilla HTML5 / CSS3 / ES6+ | Zero Node.js/npm dependencies, instant loading, 100% customizable Neo-Glassmorphism aesthetic. |
| **HTTP Client** | `requests` | Industry-standard synchronous HTTP client with configurable 10-second timeouts and exception wrapping. |
| **Configuration** | `python-dotenv` | Loads configuration from `.env` with complete isolation from version control. |
| **Test Suite** | `pytest` | Comprehensive unit and integration test suite (35 tests, 100% pass rate). |

---

## 4. Quick Start & Setup Guide

### Step 1: Open Terminal in Task Directory
```bash
cd Language_Translation_Tool_Task1
```

### Step 2: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
The project works out of the box in `dev_fallback` mode. To enable live external cloud translation, copy the template file:
```bash
cp .env.example .env
```
Select your provider in `.env`:
```ini
# Options: dev_fallback | mymemory | google | azure | deepl
TRANSLATION_PROVIDER=dev_fallback

# If using MyMemory (Free public API, no credit card required):
# TRANSLATION_PROVIDER=mymemory

# If using Google Cloud Translation:
# TRANSLATION_PROVIDER=google
# GOOGLE_TRANSLATE_API_KEY=your_key_here

# If using Microsoft Azure Translator:
# TRANSLATION_PROVIDER=azure
# AZURE_TRANSLATOR_KEY=your_key_here
# AZURE_TRANSLATOR_REGION=eastus

# If using DeepL:
# TRANSLATION_PROVIDER=deepl
# DEEPL_API_KEY=your_key_here
```

### Step 4: Run the Application Server
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 5. Running Automated Tests

Execute the complete automated test suite with `pytest`:
```bash
python -m pytest -v tests/
```
**Test Results:**
```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1
rootdir: Language_Translation_Tool_Task1
collected 35 items

tests/test_app.py ................                                       [ 45%]
tests/test_providers.py ...........                                      [ 77%]
tests/test_translation_service.py ........                               [100%]

============================= 35 passed in 0.22s ==============================
```

---

## 6. Project Documentation Index

Comprehensive documentation specifications are organized in the [`docs/`](./docs/) directory:

- [**Evaluator Demo Guide**](./docs/demo_guide.md): 2-minute step-by-step evaluation guide for CodeAlpha reviewers.
- [**Security Audit & QA Report**](./docs/security_audit.md): Complete security analysis covering secret isolation, XSS hardening, and DoS protections.
- [**Product Requirements Document (PRD)**](./docs/prd.md): Personas, functional/non-functional requirements, user stories, and acceptance criteria.
- [**System Architecture Specification**](./docs/architecture.md): Tier responsibilities, component breakdown, data flow sequence diagrams, and security design.
- [**UI/UX Design Specification**](./docs/design.md): Color tokens, typography, desktop/mobile wireframes, and component states.
- [**Architecture Decision Records (ADR)**](./docs/DECISIONS.md): ADR-001 through ADR-006 documenting technical decisions, alternatives, and trade-offs.
- [**Implementation Plan**](./docs/implementation_plan.md): 7-phase implementation blueprint with verification strategies and approval gates.
- [**Task Checklist**](./docs/task.md): Small verifiable tasks with unique IDs (`TASK-001` through `TASK-703`).
- [**Project Memory State**](./docs/memory.md): Current stage tracking, confirmed decisions, constraints, and completion log.

---

## 7. Development Status & Final Completion Log

| Phase | Phase Name | Status |
| :---: | :--- | :---: |
| **Phase 0** | Discovery & Documentation | **COMPLETED & APPROVED** |
| **Phase 1** | Project Setup & Application Skeleton | **COMPLETED & VERIFIED** |
| **Phase 2** | UI Implementation & Responsive Design | **COMPLETED & VERIFIED** |
| **Phase 3** | Translation API Integration & Secure Proxy | **COMPLETED & VERIFIED** |
| **Phase 4** | Optional Usability Features (Copy, TTS, Swap) | **COMPLETED & VERIFIED** |
| **Phase 5** | Automated Testing & Edge Case Hardening | **COMPLETED & VERIFIED** |
| **Phase 6** | Security Audit & Quality Assurance | **COMPLETED & VERIFIED** |
| **Phase 7** | GitHub Readiness & Final Submission | **COMPLETED & DELIVERED** |
