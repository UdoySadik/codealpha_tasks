# Evaluator & Demonstration Walkthrough Guide
## Project: Language Translation Tool (Task 1)
**Program:** CodeAlpha Artificial Intelligence Internship  
**Author:** AI Engineering Team  
**Last Updated:** 2026-10-27  

---

## 1. Quick Start for CodeAlpha Evaluators (Under 2 Minutes)

This project runs completely out of the box with zero external configuration needed. By default, it operates in **Explicit Development Fallback Mode**, allowing instant evaluation without requiring any paid cloud billing accounts or API keys.

### Step 1: Open Terminal in Task Directory
```bash
cd Language_Translation_Tool_Task1
```

### Step 2: Install Dependencies (If not already installed)
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application Server
```bash
python app.py
```
*Expected Console Output:*
```
[*] Starting Language Translation Tool on http://127.0.0.1:5000
[*] Active Translation Provider: dev_fallback
[*] Environment: development | Debug: True
 * Running on http://127.0.0.1:5000
```

### Step 4: Open in Web Browser
Open: **`http://127.0.0.1:5000`**

---

## 2. Interactive Feature Demonstration Checklist

Follow these quick steps to verify all required and optional features:

### Test 1: Core Translation (Default Fallback Mode)
1. In the **Source Language** card, type `"hello"`.
2. Notice the target language is **Spanish (es)**.
3. Click the gradient **"Translate"** button (or press <kbd>Ctrl</kbd> + <kbd>Enter</kbd>).
4. **Verification**: 
   - A loading spinner animates briefly.
   - The target card displays `"Hola"`.
   - The status banner displays: `"⚡ Translated using Development Fallback Mode (No external API key configured)."`.

### Test 2: Live Public API Translation (MyMemory Provider)
To test a genuine cloud translation API without a credit card:
1. Stop the server (`Ctrl + C`).
2. Create or open `.env` in `Language_Translation_Tool_Task1/`:
   ```ini
   TRANSLATION_PROVIDER=mymemory
   ```
3. Restart `python app.py`. Notice the console output:
   `[*] Active Translation Provider: mymemory`
4. Refresh `http://127.0.0.1:5000` in the browser. Notice the header badge now displays **`MYMEMORY ACTIVE`** in green!
5. Type `"Good morning, everyone!"` and click **Translate**.
6. **Verification**: The target card displays the real live translation from Translated.net: `"¡Buenos días a todos!"`.

### Test 3: Language & Text Swapping
1. Click the circular swap button (**`⇄`**) between the two cards.
2. **Verification**: 
   - The button rotates with a smooth 180° micro-animation.
   - Spanish becomes the source language and English becomes the target language.
   - The source and target text boxes swap contents.

### Test 4: Clipboard Copy Action
1. On the translated output card, click the **"Copy"** button.
2. **Verification**: The icon transitions to a checkmark (`✓`) with the label `"Copied!"` and green highlight for 2 seconds.

### Test 5: Native Text-to-Speech (TTS)
1. Click the **"Listen"** (🔊) button on either card.
2. **Verification**: The button pulses with an audio ripple effect while the browser's native speech synthesis reads the text aloud in the appropriate accent.

### Test 6: Theme Toggling (Dark / Light)
1. Click the theme button in the top right header (`🌙` / `☀️`).
2. **Verification**: The application switches fluidly between dark Neo-Glassmorphism and crisp light theme. The selection is saved in browser `localStorage`.

### Test 7: Character Counter & Limits
1. Observe the live counter under the source textarea: `X / 5000`.
2. Type text: the counter increments in real time.
3. The counter changes to amber at 4,500 characters and red at 5,000 characters.

### Test 8: Empty Input Validation
1. Click the **"Clear"** button.
2. Click **"Translate"** with empty text.
3. **Verification**: The UI displays an amber warning banner: `"Please enter text to translate."` and refocuses the cursor.

### Test 9: Translation History Drawer
1. Scroll down to the **"Recent Translations"** tray.
2. Click the header to collapse and expand the drawer (chevron animates).
3. Click **"Restore"** on any past translation to immediately reload both source and target panels.
4. Click **"✕"** to delete a single item, or **"Clear All"** to reset history.

---

## 3. Running Automated Tests

To run the complete automated test suite (35 unit and integration tests):
```bash
python -m pytest -v tests/
```
*Expected Result:*
```
============================= 35 passed in ~0.3s ==============================
```
