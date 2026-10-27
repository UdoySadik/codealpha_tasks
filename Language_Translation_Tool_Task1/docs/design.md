# UI/UX Design Specification
## Project: Language Translation Tool (Task 1)
**Program:** CodeAlpha Artificial Intelligence Internship  
**Document Status:** Pending Approval (Stage 0)  
**Author:** Lead UI/UX Designer & Frontend Engineer  
**Last Updated:** 2026-10-27  

---

## 1. Design Philosophy & User Experience Goals

The user interface of the **Language Translation Tool** is designed around clarity, high visual aesthetics, speed, and effortless ergonomics. Rather than presenting a utilitarian, stark form, the application adopts a contemporary **Neo-Glassmorphic** design with smooth micro-interactions, dark/light theme options, responsive dual-card layouts, and clear typographic hierarchy.

### Core Design Principles
1. **Focus on the Core Task**: Translation must be achievable in two clicks or a single key combination (`Ctrl+Enter`).
2. **Instant Visual Feedback**: Every interaction (hover, focus, submit, copy, clear, swap) gives immediate feedback through state transitions or subtle animations.
3. **Accessible & Ergonomic**: High contrast text, full keyboard navigability, clear ARIA labeling, and responsive reflow from 360px mobile screens to 4K desktop displays.
4. **Honest System Transparency**: Clearly distinguishes between production cloud API translations and development fallback mode via distinct visual badges.

---

## 2. Visual Direction & Design Tokens

### 2.1 Color Palette

#### Dark Mode (Default Theme)
```css
:root[data-theme="dark"] {
  /* Surfaces & Backgrounds */
  --bg-primary: #0b0f19;          /* Deep obsidian canvas */
  --bg-secondary: #131b2e;        /* Subtle slate-navy card container */
  --bg-glass: rgba(19, 27, 46, 0.75); /* Frosted glass effect */
  --bg-surface: #1e293b;          /* Input & panel background */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-focus: #6366f1;        /* Indigo glow */

  /* Text & Content */
  --text-primary: #f8fafc;        /* High-contrast crisp white */
  --text-secondary: #94a3b8;      /* Muted slate gray */
  --text-muted: #64748b;          /* Low-priority labels/counters */

  /* Brand Accents */
  --accent-primary: #6366f1;      /* Indigo vibrant */
  --accent-hover: #4f46e5;        /* Deep indigo */
  --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); /* Indigo to Violet */
  
  /* Semantic Feedback */
  --color-success: #10b981;       /* Emerald green */
  --color-warning: #f59e0b;       /* Amber */
  --color-error: #ef4444;         /* Coral red */
  --color-info: #3b82f6;          /* Sky blue */
}
```

#### Light Mode (Toggleable Theme)
```css
:root[data-theme="light"] {
  /* Surfaces & Backgrounds */
  --bg-primary: #f8fafc;          /* Clean off-white canvas */
  --bg-secondary: #ffffff;        /* Crisp white card container */
  --bg-glass: rgba(255, 255, 255, 0.85); /* Frosted glass white */
  --bg-surface: #f1f5f9;          /* Input container light gray */
  --border-subtle: #e2e8f0;
  --border-focus: #4f46e5;

  /* Text & Content */
  --text-primary: #0f172a;        /* Deep slate black */
  --text-secondary: #475569;      /* Charcoal secondary */
  --text-muted: #94a3b8;

  /* Brand Accents */
  --accent-primary: #4f46e5;
  --accent-hover: #4338ca;
  --accent-gradient: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
  
  /* Semantic Feedback */
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #2563eb;
}
```

### 2.2 Typography
- **Primary Body & UI Font**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Heading Display Font**: `'Outfit', 'Inter', sans-serif`
- **Font Scale**:
  - App Header Title: `1.5rem (24px)`, Semi-bold 600
  - Card Section Titles: `1.125rem (18px)`, Medium 500
  - Textarea Inputs: `1.0rem (16px)`, Regular 400, line-height 1.6
  - Button Labels: `0.9375rem (15px)`, Semi-bold 600
  - Micro-labels & Counters: `0.8125rem (13px)`, Regular 400

### 2.3 Elevation, Shadows & Glassmorphism
- **Glass Card Backdrop**: `backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);`
- **Card Shadow**: `0 20px 40px -15px rgba(0, 0, 0, 0.3)`
- **Hover Transitions**: `all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`
- **Border Radii**: 
  - Outer card containers: `16px`
  - Input textareas: `12px`
  - Buttons and badges: `8px`
  - Tooltips and small controls: `6px`

---

## 3. Component Hierarchy & Wireframes

### 3.1 Desktop Layout Wireframe (1024px and wider)

```
+---------------------------------------------------------------------------------------+
|  [Logo] PolyGlot AI | CodeAlpha Translation Tool            [Provider Badge] [Theme] |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +-------------------------------------+   +----+   +-------------------------------+ |
|  | Source Language: [ English (en) v ] |   | <->|   | Target: [ Spanish (es)    v ] | |
|  +-------------------------------------+   +----+   +-------------------------------+ |
|  |                                     |            |                               | |
|  |  Enter or paste text to translate...|            |  Translated text appears here | |
|  |                                     |            |  with formatting intact...    | |
|  |                                     |            |                               | |
|  |                                     |            |                               | |
|  |                                     |            |                               | |
|  +-------------------------------------+            +-------------------------------+ |
|  | [Clear]        28 / 5000 chars [TTS]|            | [TTS]            [Copy Result]| |
|  +-------------------------------------+            +-------------------------------+ |
|                                                                                       |
|             [ =================== TRANSLATE (Ctrl+Enter) =================== ]        |
|                                                                                       |
|  +---------------------------------------------------------------------------------+  |
|  | [i] Notification Banner: Development Fallback Active (or Success / Error state) |  |
|  +---------------------------------------------------------------------------------+  |
|                                                                                       |
|  [v] View Recent Translations (History Drawer: 5 items)                               |
+---------------------------------------------------------------------------------------+
|  Footer: Built for CodeAlpha AI Internship | Secure Server Proxy | Python Flask & JS  |
+---------------------------------------------------------------------------------------+
```

### 3.2 Mobile Layout Wireframe (Single Column, < 768px)

```
+-------------------------------------------+
| [Logo] PolyGlot AI     [Provider] [Theme] |
+-------------------------------------------+
| Source: [ English (en)                  v]|
+-------------------------------------------+
| Enter text here...                        |
|                                           |
|                                           |
+-------------------------------------------+
| [Clear]          142 / 5000 chars    [TTS]|
+-------------------------------------------+
|           [   <-> Swap Languages   ]      |
+-------------------------------------------+
| Target: [ French (fr)                   v]|
+-------------------------------------------+
| Le texte traduit apparaîtra ici...        |
|                                           |
|                                           |
+-------------------------------------------+
| [TTS]                        [Copy Result]|
+-------------------------------------------+
|       [ ======= TRANSLATE ======= ]       |
+-------------------------------------------+
| [!] Banner / Error Notice                 |
+-------------------------------------------+
| [v] Recent Translation History            |
+-------------------------------------------+
```

---

## 4. Detailed Component Behavior & States

### 4.1 Language Selection Bars & Swap Action
- **Source Language Dropdown**:
  - First option: `Auto-Detect (Detect Language)`.
  - Followed by top common languages: English, Spanish, French, German, Mandarin Chinese, Arabic, Hindi, Japanese, Russian, Portuguese, etc. (30+ total).
  - Searchable or quick-jump via keyboard typing.
- **Target Language Dropdown**:
  - List of 30+ supported target languages with native and English names (e.g. `Español (Spanish)`).
- **Swap Languages Button (`<->`)**:
  - Centered between the dropdowns on desktop; stacked horizontally on mobile.
  - Clicking smoothly swaps source and target selections.
  - If source was `Auto-Detect`, the swap button is either disabled or assigns the detected source language to the new target.
  - Reverses the contents of input and output text boxes if translations already exist.

### 4.2 Source Input Textarea
- **Placeholder**: `"Type or paste text to translate here..."`
- **Auto-expansion**: Fixed minimum height (`180px`), vertical expansion or graceful internal scrollbar for long texts.
- **Character Counter**:
  - Live count: `X / 5000 characters`.
  - Normal state: Muted gray text.
  - Warning state (at 4,500 chars): Amber text.
  - Overflow state (at 5,000 chars): Red text and prevents additional characters.
- **Clear Action**: A subtle trash/cross icon to immediately empty the textarea and reset output.
- **Keyboard Shortcut**: `Ctrl + Enter` (or `Cmd + Enter` on macOS) triggers immediate translation without needing to click.

### 4.3 Target Output Panel
- **Placeholder / Empty State**: `"Translation will appear here..."` in muted text with a gentle translation icon.
- **Read-Only**: Target panel prevents accidental manual typing to protect translation authenticity.
- **Copy Button**:
  - Default: Clipboard icon with `"Copy"`.
  - Clicked State: Changes to green checkmark icon with `"Copied!"` for 2,000 ms.
  - Graceful fallback: If Clipboard API is restricted by browser permissions, selects all text for manual `Ctrl+C`.
- **Text-to-Speech (TTS) Button**:
  - Speaker icon button.
  - When clicked, utilizes browser `window.speechSynthesis` configured with the target language code.
  - Active audio state: Pulsing speaker icon while speech is actively playing; clicking again cancels playback.

### 4.4 Translate Button & Loading State
- **Primary CTA Button**: Prominent, centered or aligned with gradient background (`linear-gradient(135deg, #6366f1, #a855f7)`).
- **Idle State**: Text reads `"Translate"` with a rightward translation icon.
- **In-Flight Loading State**:
  - Button text changes to `"Translating..."`.
  - Icon replaced by a smooth rotating SVG spinner.
  - Button disabled (`opacity: 0.75; cursor: not-allowed;`) to prevent duplicate submissions.
  - Target panel displays a subtle shimmer/skeleton loader animation.

### 4.5 Error and Notification Banners
- Non-intrusive banner positioned beneath the translate button or directly atop the cards.
- **Error Types**:
  - *Network Timeout*: `"Network timed out. Please check your internet connection."`
  - *Empty Input*: `"Please enter text before requesting a translation."`
  - *Upstream Quota*: `"Provider rate limit reached. Please wait a moment."`
  - *Dev Fallback Notice*: `"Development Mode: No external API key found. Using local fallback translation engine."` (styled in calming blue/indigo with a clear badge).

### 4.6 Translation History Drawer (Optional Enhancement)
- Collapsible tray at the bottom of the page.
- Stores the last 10 successful translation entries in browser `localStorage`.
- Each entry displays:
  - Source snippet and target snippet.
  - Language pair badge (e.g., `EN -> ES`).
  - Timestamp (e.g., `2 mins ago`).
  - Action buttons: "Restore" (populates the main panels) and "Delete".
  - "Clear History" button to wipe stored entries.

---

## 5. Accessibility (a11y) & Usability Compliance

1. **Semantic Hierarchy**: Single `<h1>` tag for the page title; landmark regions (`<header>`, `<main>`, `<footer>`, `<section>`).
2. **Keyboard Traversal**:
   - Tab order flows logically: Source dropdown -> Text input -> Clear -> Target dropdown -> Translate button -> Copy button -> Audio button.
   - All interactive controls have distinct `:focus-visible` outlines (2px solid `--border-focus`).
3. **Screen Reader Support**:
   - `aria-label` attributes on icon-only buttons (`"Copy translated text"`, `"Listen to translation"`, `"Swap languages"`).
   - `aria-live="polite"` on output translation container so screen readers automatically announce new translations when available.
4. **Color Contrast**:
   - Text-to-background contrast ratio exceeds 4.5:1 across both Dark and Light themes.
