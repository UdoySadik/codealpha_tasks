# 🎨 UI/UX Design Specification — FAQ Chatbot

> **Document Version:** 1.0.0  
> **Status:** Stage 0 Blueprint (Pending Approval)  
> **Application Type:** Streamlit Conversational AI Web Interface  

---

## 1. UI/UX Core Goals & Design Philosophy

1. **Clarity & Immediacy**: Users understand the chatbot's domain, scope, and capabilities within 3 seconds of landing.
2. **Transparent AI Feedback**: Answers distinguish between confident FAQ matches and fallback responses with clear visual indicators.
3. **Conversational Ergonomics**: Smooth auto-scrolling, clear visual separation between user and assistant messages, and comfortable readability.
4. **Resilience & Graceful Degradation**: Zero silent failures, informative banners for edge cases, and empty input handling.
5. **Accessibility First (WCAG 2.1 AA)**: Minimum 4.5:1 contrast ratios, keyboard navigability, semantic structure, and screen-reader-friendly markdown rendering.

---

## 2. Visual Design System & Palette

### 2.1 Color Tokens
The UI adopts a contemporary **Deep Slate & Indigo** palette designed to work harmoniously in both dark and light modes while giving an authoritative, academic feel.

| Token Name | Hex Code | HSL Equivalent | Role / Semantic Meaning |
| :--- | :--- | :--- | :--- |
| `--color-primary` | `#4F46E5` | `hsl(244, 75%, 59%)` | Primary brand accent (Indigo), active buttons, user bubbles |
| `--color-primary-light` | `#6366F1` | `hsl(239, 84%, 67%)` | Hover states, interactive highlights |
| `--color-background` | `#0F172A` | `hsl(222, 47%, 11%)` | Canvas background (Dark Slate) |
| `--color-surface` | `#1E293B` | `hsl(217, 33%, 17%)` | Card surfaces, sidebar background, assistant bubbles |
| `--color-surface-border` | `#334155` | `hsl(215, 25%, 27%)` | Container dividers, input border |
| `--color-text-main` | `#F8FAFC` | `hsl(210, 40%, 98%)` | High-contrast primary body text (14.2:1 contrast) |
| `--color-text-muted` | `#94A3B8` | `hsl(215, 20%, 65%)` | Timestamps, subtitles, confidence metrics |
| `--color-success` | `#10B981` | `hsl(160, 84%, 39%)` | High confidence match indicator |
| `--color-warning` | `#F59E0B` | `hsl(38, 92%, 50%)` | Moderate confidence / fallback advisory |
| `--color-error` | `#EF4444` | `hsl(0, 84%, 60%)` | System error alert, missing data warning |

### 2.2 Typography Hierarchy
- **Primary Typeface**: Inter / System UI Font Stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif`).
- **Code / Monospace**: JetBrains Mono, Fira Code, Consolas.

| Element | Font Size | Font Weight | Line Height | Tracking |
| :--- | :--- | :--- | :--- | :--- |
| **App Title (`h1`)** | `1.875rem` (30px) | `700` (Bold) | `1.2` | `-0.02em` |
| **Section Header (`h2`)** | `1.375rem` (22px) | `600` (Semi-bold) | `1.3` | `-0.01em` |
| **Subheader (`h3`)** | `1.125rem` (18px) | `600` (Semi-bold) | `1.4` | `0` |
| **Chat Message Body** | `1.000rem` (16px) | `400` (Regular) | `1.55` | `0` |
| **Meta / Score Tag** | `0.812rem` (13px) | `500` (Medium) | `1.4` | `+0.01em` |

---

## 3. Layout Structure & Wireframe

```text
+------------------------------------------------------------------------------+
| 🎓 Campus Services FAQ Assistant                      [Settings / Help]      |
| "Ask anything about academic registrations, fees, campus IDs, and services"  |
+------------------------------------------------------------------------------+
|  SIDEBAR (Collapsible)    |  MAIN CHAT CONTAINER                             |
|                           |                                                  |
|  📚 Knowledge Base Stats  |  [Empty State: Welcome Banner & Suggested Chips] |
|  - Domain: Campus Services|  +---------------------------------------------+ |
|  - FAQs Indexed: 25 items |  | 💡 "How do I register for courses?"         | |
|  - Categories: 5          |  | 💳 "What are the payment deadlines?"         | |
|                           |  | 🆔 "Where can I get my student ID card?"    | |
|  ⚙️ Match Engine Controls  |  +---------------------------------------------+ |
|  - Threshold Slider: 0.30 |                                                  |
|  - Show Confidence: [x]   |  👤 USER:                                        |
|                           |  Can I get a replacement ID card if lost?        |
|  🗑️ Actions               |                                                  |
|  [ Clear Conversation ]   |  🤖 ASSISTANT (Match: 0.68 | ID: id_services_02):|
|                           |  Replacement ID cards are issued at the Campus   |
|                           |  Security & Services Office. Bring a photo ID... |
|                           |                                                  |
+---------------------------+--------------------------------------------------+
|  [💬 Ask a question about campus services, tuition, or registration...] [Send]|
+------------------------------------------------------------------------------+
```

---

## 4. Chat Component Specifications

### 4.1 Message Bubbles
- **User Messages**:
  - Align: Right-biased or standard chat container with user avatar icon (`🧑‍🎓`).
  - Background: Primary accent subtle tint (`rgba(79, 70, 229, 0.15)`) with an indigo border.
  - Text alignment: Left-aligned for natural reading; right anchor.
- **Assistant Messages**:
  - Align: Left-biased container with bot avatar (`🤖`).
  - Background: Surface card background (`#1E293B`).
  - Badges: Optional meta bar underneath displaying category tag and similarity confidence chip (e.g., `Confidence: 74%`).

### 4.2 Interactive Suggestion Chips (Empty State)
When the session has zero messages:
- Display an inviting hero card with an overview icon.
- Present 3 to 4 clickable prompt buttons that immediately populate and submit standard queries (e.g., *"How do I register for classes?"*, *"How do I view my semester grades?"*).

### 4.3 Input Area
- Position: Sticky bottom container utilizing `st.chat_input`.
- Placeholder: *"Type your campus question here (e.g., 'How do I pay tuition?')..."*
- Interaction: Pressing `Enter` or clicking the submit icon dispatches the message instantly, triggering the response cycle.

### 4.4 Status States
- **Normal Match State**: Renders clean markdown answer text accompanied by confidence metadata.
- **Fallback State**: Displays a helpful notice icon (`🔍`), a polite explanation that no FAQ matched the query, and 2-3 suggestions on how to rephrase.
- **Empty Query Warning**: If a user submits spaces or empty characters, a temporary `st.warning` notification clarifies that input is required.
- **System Error State**: If `faqs.json` is missing or unreadable, a persistent `st.error` alert guides the user or administrator with remediation steps.

---

## 5. Responsive Behavior

- **Desktop (> 1024px)**: Full dual-column layout with pinned sidebar containing administrative metadata and similarity controls.
- **Tablet (768px – 1024px)**: Sidebar starts collapsed by default, expandable via hamburger toggle. Chat area retains 720px max-width centered reading container.
- **Mobile (< 768px)**: 100% width viewport, stacked elements, full-width touch targets for suggested prompts, and compact chat padding.

---

## 6. Accessibility & Usability (WCAG 2.1 AA Checklist)

- [x] **Color Contrast**: All text elements achieve a contrast ratio $\ge 4.5:1$ against their respective backgrounds.
- [x] **Non-Color Indicators**: Fallback messages and system alerts use icons and text labels in addition to color.
- [x] **Keyboard Navigation**: Standard browser focus outlines preserved across all interactive controls (`st.chat_input`, suggestion chips, sidebar sliders).
- [x] **Text Scaling**: Layout supports 200% browser zoom without clipping or broken layout grids.
- [x] **No Flashing Content**: Zero strobe or flashing animations; smooth CSS transitions capped at `< 300ms`.
