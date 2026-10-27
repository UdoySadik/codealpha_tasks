# PolyGlot AI — Language Translation Tool
### Task 1 | CodeAlpha Artificial Intelligence Internship

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Stage%200%20%7C%20Architecture%20Review-orange.svg)](#development-status)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Interface](https://img.shields.io/badge/UI-Neo--Glassmorphic%20SPA-purple.svg)](#uiux-design)

---

## 1. Project Overview

The **Language Translation Tool** is a clean, secure, and modern translation application engineered as part of the **CodeAlpha Artificial Intelligence Internship**. 

The system provides a seamless bridge across language barriers by coupling a high-performance Python server proxy with an elegant, responsive web interface. It bridges the gap between powerful cloud translation engines (such as Google Cloud Translation API, Microsoft Azure Translator, and DeepL) and the end user, while ensuring that API keys are strictly protected and never exposed to the client.

> **Project Stage Notice:** This project is currently in **Stage 0 (Discovery & Documentation)**. The documentation and architectural blueprints are complete and pending formal user authorization. Application source code and third-party dependencies have not yet been implemented.

---

## 2. Planned Features

### Core Requirements
- **Intuitive Text Input**: Multi-line textarea supporting up to 5,000 Unicode characters with pasting support.
- **Source Language Detection**: Selection of 30+ major languages plus an intelligent "Auto-Detect" mode.
- **Target Language Selection**: Alphabetically organized, searchable language picker covering major global languages.
- **Translate Button & Keyboard Shortcuts**: Execute translation via dedicated action button or `Ctrl + Enter`.
- **Genuine Cloud API Integration**: Secure server-side translation proxy supporting Google Cloud Translation API, Microsoft Azure Translator, DeepL API, and MyMemory.
- **Honest Development Fallback Mode**: When cloud API credentials are not provided, an explicit local fallback provider executes and clearly flags translations with a `Development Fallback` UI badge.
- **Clear Output Display**: Clean, scrollable translated text area preserving punctuation, spacing, and formatting.
- **Loading & State Indicators**: Smooth animated spinner and disabled submit state during pending network requests.
- **Comprehensive Error Handling**: Actionable, user-friendly error banners for empty input, upstream rate limits, and network dropouts.

### Approved Optional Usability Enhancements
- **One-Click Clipboard Copy**: Copy translated output instantly with an animated "Copied!" confirmation tooltip.
- **Language Swap (`<->`)**: Instantly reverse source and target languages and swap their text contents.
- **Text-to-Speech (TTS)**: In-browser speech synthesis for audio pronunciation in native accents.
- **Live Character Counter**: Dynamic visual indicator (`X / 5000 characters`) with amber/red threshold alerts.
- **Clear Action**: One-click reset for textareas, character counter, and notification banners.
- **Dark & Light Mode**: Fluid theme toggle with persistent user preference stored in `localStorage`.
- **Translation History**: In-session drawer storing the last 10 translations with one-click restoration.

---

## 3. Planned Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend Service** | Python 3.13 + Flask | Minimalist, robust, standard library feel, serves both API routes and static frontend assets with zero build complexity. |
| **Frontend UI** | Modern Vanilla HTML5 / CSS3 / ES6+ | Zero Node.js/npm dependencies, instant loading, 100% customizable Neo-Glassmorphism aesthetic. |
| **HTTP Client** | `requests` | Industry-standard synchronous HTTP client with configurable timeouts and error handling. |
| **Configuration** | `python-dotenv` | Loads configuration from `.env` with complete isolation from version control. |
| **Test Suite** | `pytest` | Concise syntax, rich fixtures, and unit/integration testing coverage. |

---

## 4. Planned Installation & Setup Guide

*(Note: These instructions outline the planned operational workflow following Phase 1 approval.)*

### Step 1: Clone Repository & Navigate to Directory
```bash
cd Language_Translation_Tool_Task1
```

### Step 2: Create and Activate a Python Virtual Environment
```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
Open `.env` in your text editor and select your translation provider:
```ini
# Choose: dev_fallback | google | azure | deepl | mymemory
TRANSLATION_PROVIDER=dev_fallback

# If using Google Cloud Translation:
GOOGLE_TRANSLATE_API_KEY=your_actual_key_here

# If using Microsoft Azure Translator:
AZURE_TRANSLATOR_KEY=your_actual_key_here
AZURE_TRANSLATOR_REGION=eastus

# If using DeepL:
DEEPL_API_KEY=your_actual_key_here
```

### Step 5: Run the Application Server
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 5. Translation API Configuration & Pricing Matrix

| Provider | Authentication Method | Quota / Free Tier | Estimated Setup Time |
| :--- | :--- | :--- | :--- |
| **Development Fallback** | None (Built-in) | Unlimited / 100% Free | 0 Minutes (Default) |
| **MyMemory Public API** | Free REST (Optional Email) | 5,000 chars/day (anonymous) *(50k with email)* | 1 Minute |
| **Google Cloud Translation** | API Key or Service Account JSON | 500,000 chars/month free *(UNVERIFIED live quota)* | 10 Minutes (GCP Project + Billing) |
| **Microsoft Azure Translator** | Cognitive Services Key + Region | 2,000,000 chars/month free *(UNVERIFIED live quota)* | 10 Minutes (Azure Portal) |
| **DeepL API** | API Auth Key (`:fx`) | 500,000 chars/month free *(UNVERIFIED live quota)* | 5 Minutes (DeepL Free Account) |

---

## 6. Project Documentation Index

Comprehensive project planning specifications are maintained in the [`docs/`](./docs/) directory:

- [**Product Requirements Document (PRD)**](./docs/prd.md): Personas, functional/non-functional requirements, user stories, and acceptance criteria.
- [**System Architecture Specification**](./docs/architecture.md): Tier responsibilities, component breakdown, data flow sequence diagrams, and security design.
- [**UI/UX Design Specification**](./docs/design.md): Color tokens, typography, desktop/mobile wireframes, and component states.
- [**Architecture Decision Records (ADR)**](./docs/DECISIONS.md): ADR-001 through ADR-006 documenting technical decisions, alternatives, and trade-offs.
- [**Implementation Plan**](./docs/implementation_plan.md): 7-phase implementation blueprint with verification strategies and approval gates.
- [**Task Checklist**](./docs/task.md): Small verifiable tasks with unique IDs (`TASK-001` through `TASK-703`).
- [**Project Memory State**](./docs/memory.md): Current stage tracking, confirmed decisions, constraints, and next actions.

---

## 7. Development Status & Strict Approval Gates

| Phase | Phase Name | Status |
| :---: | :--- | :---: |
| **Phase 0** | Discovery & Documentation | **COMPLETED (Pending User Review)** |
| **Phase 1** | Project Setup & Application Skeleton | PENDING APPROVAL |
| **Phase 2** | UI Implementation & Responsive Design | PENDING |
| **Phase 3** | Translation API Integration & Secure Proxy | PENDING |
| **Phase 4** | Optional Usability Features (Copy, TTS, Swap) | PENDING |
| **Phase 5** | Automated Testing & Edge Case Hardening | PENDING |
| **Phase 6** | Security Audit & Quality Assurance | PENDING |
| **Phase 7** | GitHub Readiness & Final Submission | PENDING |

To authorize the commencement of Phase 1, the user must respond with:
```
APPROVE DOCUMENTATION
```
