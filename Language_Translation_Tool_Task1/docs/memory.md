# Project Memory & Context State
## Project: Language Translation Tool (Task 1)
**Program:** CodeAlpha Artificial Intelligence Internship  
**Document Status:** Pending Approval (Stage 0)  
**Author:** AI Project Assistant  
**Last Updated:** 2026-10-27  

---

## 1. Project Overview & Current Stage
- **Repository Context**: `c:\Users\Udoy\Desktop\Varsity\codealpha_tasks\Language_Translation_Tool_Task1`
- **Current Stage**: **Stage 0 — Discovery and Documentation (ACTIVE / PENDING USER APPROVAL)**
- **Implementation Status**: Zero application code written. No packages installed. No servers running. Documentation blueprint prepared and awaiting mandatory user review.
- **Next Authorized Action**: Awaiting the user's explicit command **`APPROVE DOCUMENTATION`** before starting Phase 1.

---

## 2. Confirmed & Proposed Architectural Decisions

| Decision Area | Status | Choice | Key Rationale |
| :--- | :--- | :--- | :--- |
| **System Architecture** | `PROPOSED` | Single-process Flask server + Vanilla HTML5/CSS3/ES6 SPA | Minimizes setup friction for evaluators; eliminates Node.js/npm dependencies; provides 100% aesthetic control. |
| **Translation Provider** | `PROPOSED` | Pluggable Provider Pattern (Google, Azure, DeepL, MyMemory) + Explicit Dev Fallback | Guarantees genuine cloud API execution when keys are present while providing an honest, explicitly badged development fallback when keys are absent. |
| **Security & Secrets** | `PROPOSED` | Server-side `.env` via `python-dotenv`; zero client-side keys | Protects credentials from being leaked to client browser or committed to Git. |
| **Styling & Theme** | `PROPOSED` | Vanilla CSS Neo-Glassmorphism with CSS Variables (Dark/Light) | Creates a stunning visual impression ("wow factor") with zero CSS framework bloat. |
| **Audio / TTS** | `PROPOSED` | Client-Side Web Speech API (`window.speechSynthesis`) | Eliminates server-side audio rendering latency and external TTS charges. |

---

## 3. Strict Project Constraints & Immutable Rules
1. **Approval Gates**: Never begin implementation before the user explicitly types `APPROVE DOCUMENTATION`. Never advance between phases without the user explicitly typing `CONTINUE`.
2. **Honesty in Translation**: Never disguise a local mock response as a real API translation. When running without external API keys, the system must clearly badge the output as `Development Fallback Mode`.
3. **No Secret Commits**: Never hardcode API keys or commit `.env` files to version control. Maintain `.env.example` as the single source of configuration truth.
4. **No Premature Claims**: Never claim an unimplemented feature works or that automated tests pass unless actually verified.

---

## 4. Environment & Tooling Context
- **Operating System**: Windows 11
- **Python Version**: Python 3.13.5 (Verified installed)
- **Version Control**: Git on branch `main`
- **Target Web Technologies**: Python (Flask), HTML5, Vanilla CSS3, Modern JavaScript (ES6+)

---

## 5. Unresolved Questions & User Decisions for Review
1. **Primary Backend Framework**: Flask is proposed as the primary recommendation due to its lightweight simplicity and standard curriculum familiarity. FastAPI is available if asynchronous I/O is preferred.
2. **Preferred Translation Provider for Testing**: Does the user have an active Google Cloud Translation API key, Microsoft Azure Translator key, DeepL key, or do they plan to test primarily with the free MyMemory API and the built-in Development Fallback Provider?

---

## 6. Execution Progress Summary

- [x] **Stage 0: Discovery & Documentation** (Completed all 10 planning documents)
- [ ] **Phase 1: Environment Setup & Application Skeleton** (Pending user approval)
- [ ] **Phase 2: UI Implementation & Responsive Design** (Pending)
- [ ] **Phase 3: Translation API Integration & Secure Proxy** (Pending)
- [ ] **Phase 4: Optional Usability Features** (Pending)
- [ ] **Phase 5: Automated Testing & Edge Cases** (Pending)
- [ ] **Phase 6: Security Audit & Quality Assurance** (Pending)
- [ ] **Phase 7: GitHub Readiness & Final Submission** (Pending)
