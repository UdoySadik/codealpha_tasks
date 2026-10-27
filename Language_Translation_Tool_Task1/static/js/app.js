/**
 * PolyGlot AI — Main Frontend Application Controller
 * Handles Theme, Real-time Counters, Speech Synthesis, Clipboard,
 * Keyboard Shortcuts, and Translation State Management.
 */

document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Elements ---
    const sourceText = document.getElementById("source-text");
    const targetText = document.getElementById("target-text");
    const sourceLang = document.getElementById("source-language");
    const targetLang = document.getElementById("target-language");

    const btnTranslate = document.getElementById("btn-translate");
    const btnTranslateText = document.getElementById("btn-translate-text");
    const btnSwap = document.getElementById("btn-swap");
    const btnClear = document.getElementById("btn-clear");
    const btnCopy = document.getElementById("btn-copy");
    const copyIcon = document.getElementById("copy-icon");
    const copyText = document.getElementById("copy-text");

    const btnTtsSource = document.getElementById("btn-tts-source");
    const btnTtsTarget = document.getElementById("btn-tts-target");
    const charCounter = document.getElementById("char-counter");

    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");

    const providerBadge = document.getElementById("provider-badge");
    const providerName = document.getElementById("provider-name");

    const statusBanner = document.getElementById("status-banner");
    const statusIcon = document.getElementById("status-icon");
    const statusMessage = document.getElementById("status-message");

    const historyList = document.getElementById("history-list");
    const historyCount = document.getElementById("history-count");
    const btnClearHistory = document.getElementById("btn-clear-history");

    // --- State Variables ---
    let lastDetectedLang = null;
    let isSpeaking = false;
    let hasTranslated = false;
    const MAX_CHARS = 5000;

    // --- 1. Initialize Language Selectors ---
    if (typeof populateLanguageSelectors === "function") {
        populateLanguageSelectors(sourceLang, targetLang, "auto", "es");
    }

    // --- 2. Theme Management (Dark / Light) ---
    const savedTheme = localStorage.getItem("polyglot_theme") || "dark";
    applyTheme(savedTheme);

    themeToggle.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        applyTheme(newTheme);
    });

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("polyglot_theme", theme);
        themeIcon.textContent = theme === "dark" ? "🌙" : "☀️";
        themeToggle.setAttribute("title", `Switch to ${theme === "dark" ? "Light" : "Dark"} Mode`);
    }

    // --- 3. Live Character Counter & Input Sync ---
    sourceText.addEventListener("input", () => {
        updateCharCounter();
        if (!sourceText.value.trim()) {
            targetText.value = "";
            hasTranslated = false;
        }
    });

    function updateCharCounter() {
        const length = sourceText.value.length;
        charCounter.textContent = `${length} / ${MAX_CHARS}`;

        charCounter.classList.remove("warning", "danger");
        if (length >= MAX_CHARS) {
            charCounter.classList.add("danger");
        } else if (length >= 4500) {
            charCounter.classList.add("warning");
        }
    }

    // --- 4. Clear Fields Action ---
    btnClear.addEventListener("click", () => {
        sourceText.value = "";
        targetText.value = "";
        hasTranslated = false;
        updateCharCounter();
        hideStatusBanner();
        sourceText.focus();
    });

    // --- 5. Language Swapping ---
    btnSwap.addEventListener("click", () => {
        const currentSource = sourceLang.value;
        const currentTarget = targetLang.value;

        // If source is auto, swap target into source, and use detected or default for target
        if (currentSource === "auto") {
            const resolvedTarget = lastDetectedLang || "en";
            sourceLang.value = currentTarget;
            targetLang.value = resolvedTarget;
        } else {
            sourceLang.value = currentTarget;
            targetLang.value = currentSource;
        }

        // Swap contents if both or either has text
        const tempText = sourceText.value;
        sourceText.value = targetText.value;
        targetText.value = tempText;

        updateCharCounter();
        showStatusBanner("Languages and text swapped.", "info", 2000);

        // Auto-translate if user already performed initial translation
        if (hasTranslated && sourceText.value.trim()) {
            executeTranslation();
        }
    });

    // --- 6. Clipboard Copying ---
    btnCopy.addEventListener("click", async () => {
        const textToCopy = targetText.value.trim();
        if (!textToCopy) {
            showStatusBanner("No translated text to copy.", "warning", 2500);
            return;
        }

        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(textToCopy);
            } else {
                // Fallback for non-https or older browser contexts
                targetText.select();
                document.execCommand("copy");
            }

            // Visual feedback on button
            btnCopy.classList.add("copied");
            copyIcon.textContent = "✓";
            copyText.textContent = "Copied!";

            setTimeout(() => {
                btnCopy.classList.remove("copied");
                copyIcon.textContent = "📋";
                copyText.textContent = "Copy";
            }, 2000);
        } catch (err) {
            showStatusBanner("Unable to copy to clipboard automatically.", "error", 3000);
        }
    });

    // --- 7. Text-to-Speech (TTS via Web Speech API) ---
    btnTtsSource.addEventListener("click", () => {
        const text = sourceText.value.trim();
        const langCode = sourceLang.value === "auto" ? "en" : sourceLang.value;
        playSpeech(text, langCode, btnTtsSource);
    });

    btnTtsTarget.addEventListener("click", () => {
        const text = targetText.value.trim();
        const langCode = targetLang.value;
        playSpeech(text, langCode, btnTtsTarget);
    });

    let activeAudio = null;

    function playSpeech(text, langCode, buttonElement) {
        if (!text) {
            showStatusBanner("No text available to play.", "warning", 2500);
            return;
        }

        // Toggle: stop if already speaking
        if (activeAudio) {
            activeAudio.pause();
            activeAudio = null;
            resetSpeechButtons();
            return;
        }

        if (window.speechSynthesis && window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            resetSpeechButtons();
            return;
        }

        // BCP-47 tag mappings
        const bcpMap = {
            bn: "bn-BD", hi: "hi-IN", es: "es-ES", fr: "fr-FR", de: "de-DE",
            ar: "ar-SA", zh: "zh-CN", ja: "ja-JP", ru: "ru-RU", pt: "pt-BR",
            it: "it-IT", ko: "ko-KR", tr: "tr-TR", nl: "nl-NL", sv: "sv-SE"
        };
        const bcpTag = bcpMap[langCode] || langCode;

        let hasNativeVoice = false;
        if ("speechSynthesis" in window) {
            const voices = window.speechSynthesis.getVoices();
            hasNativeVoice = voices.some(v => v.lang.toLowerCase().startsWith(langCode));
        }

        if (hasNativeVoice) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = bcpTag;

            const voices = window.speechSynthesis.getVoices();
            const matchingVoice = voices.find(v => v.lang.toLowerCase().startsWith(langCode));
            if (matchingVoice) {
                utterance.voice = matchingVoice;
            }

            buttonElement.classList.add("speaking");

            utterance.onend = () => {
                buttonElement.classList.remove("speaking");
            };

            utterance.onerror = () => {
                buttonElement.classList.remove("speaking");
                // Fallback to server audio if browser voice fails
                playServerAudio(text, langCode, buttonElement);
            };

            window.speechSynthesis.speak(utterance);
        } else {
            // Direct server audio fallback for languages without native Windows voice
            playServerAudio(text, langCode, buttonElement);
        }
    }

    function playServerAudio(text, langCode, buttonElement) {
        buttonElement.classList.add("speaking");
        const audioUrl = `/api/tts?text=${encodeURIComponent(text.slice(0, 300))}&lang=${encodeURIComponent(langCode)}`;
        activeAudio = new Audio(audioUrl);

        activeAudio.play().then(() => {
            showStatusBanner("Playing audio pronunciation...", "info", 2000);
        }).catch(() => {
            buttonElement.classList.remove("speaking");
            activeAudio = null;
            showStatusBanner("Could not play audio pronunciation for this language.", "warning", 3000);
        });

        activeAudio.onended = () => {
            buttonElement.classList.remove("speaking");
            activeAudio = null;
        };

        activeAudio.onerror = () => {
            buttonElement.classList.remove("speaking");
            activeAudio = null;
            showStatusBanner("Audio voice unavailable.", "warning", 3000);
        };
    }

    function resetSpeechButtons() {
        btnTtsSource.classList.remove("speaking");
        btnTtsTarget.classList.remove("speaking");
        if (activeAudio) {
            activeAudio.pause();
            activeAudio = null;
        }
    }

    // --- 8. Keyboard Shortcuts ---
    document.addEventListener("keydown", (e) => {
        // Ctrl + Enter or Cmd + Enter to translate
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            btnTranslate.click();
        }
        // Esc to dismiss status banner
        if (e.key === "Escape") {
            hideStatusBanner();
        }
    });

    // --- 9. Primary Translation Execution & Auto-Translate ---
    async function executeTranslation() {
        const text = sourceText.value.trim();
        const source_lang = sourceLang.value;
        const target_lang = targetLang.value;

        // Validate non-empty
        if (!text) {
            showStatusBanner("Please enter text to translate.", "warning", 3000);
            sourceText.focus();
            return;
        }

        // Validate max length
        if (text.length > MAX_CHARS) {
            showStatusBanner(`Text exceeds maximum limit of ${MAX_CHARS} characters.`, "error", 3500);
            return;
        }

        // Set Loading State
        setLoadingState(true);
        hideStatusBanner();

        try {
            const response = await fetch("/api/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    source_lang: source_lang,
                    target_lang: target_lang
                })
            });

            if (response.ok) {
                const data = await response.json();
                targetText.value = data.translated_text || "";
                lastDetectedLang = data.detected_source_lang || null;
                hasTranslated = true;

                // Check for fallback indicator
                if (data.is_fallback) {
                    showStatusBanner("⚡ Translated using Development Fallback Mode (No external API key configured).", "info");
                }

                // Add to history
                saveToHistory({
                    source: text,
                    target: data.translated_text,
                    sourceLang: data.detected_source_lang || source_lang,
                    targetLang: target_lang,
                    timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                });
            } else {
                const errData = await response.json().catch(() => ({}));
                const errMsg = errData.error || `Translation request failed (HTTP ${response.status})`;
                showStatusBanner(errMsg, "error");
            }
        } catch (networkErr) {
            showStatusBanner("Network error: Unable to connect to translation server. Please check your connection.", "error");
        } finally {
            setLoadingState(false);
        }
    }

    btnTranslate.addEventListener("click", executeTranslation);

    // Auto-translate on target or source language change after initial translation
    targetLang.addEventListener("change", () => {
        if (hasTranslated && sourceText.value.trim()) {
            executeTranslation();
        }
    });

    sourceLang.addEventListener("change", () => {
        if (hasTranslated && sourceText.value.trim()) {
            executeTranslation();
        }
    });

    function setLoadingState(loading) {
        if (loading) {
            btnTranslate.classList.add("loading");
            btnTranslate.disabled = true;
            btnTranslateText.textContent = "Translating...";
        } else {
            btnTranslate.classList.remove("loading");
            btnTranslate.disabled = false;
            btnTranslateText.textContent = "Translate";
        }
    }

    // --- 10. Status / Alert Banner Helpers ---
    let bannerTimeout = null;

    function showStatusBanner(message, type = "info", autoDismissMs = null) {
        if (bannerTimeout) clearTimeout(bannerTimeout);

        statusMessage.textContent = message;
        statusBanner.className = `status-banner visible ${type}`;

        const icons = {
            info: "ℹ️",
            warning: "⚠️",
            error: "❌"
        };
        statusIcon.textContent = icons[type] || "ℹ️";

        if (autoDismissMs) {
            bannerTimeout = setTimeout(hideStatusBanner, autoDismissMs);
        }
    }

    function hideStatusBanner() {
        statusBanner.className = "status-banner";
        if (bannerTimeout) clearTimeout(bannerTimeout);
    }

    // --- 11. Fetch System Health & Provider Metadata on Startup ---
    async function fetchSystemHealth() {
        try {
            const res = await fetch("/api/health");
            if (res.ok) {
                const data = await res.json();
                if (data.is_dev_fallback) {
                    providerBadge.className = "provider-badge fallback";
                    providerName.textContent = "Dev Fallback Mode";
                } else {
                    providerBadge.className = "provider-badge live";
                    providerName.textContent = `${data.active_provider.toUpperCase()} Active`;
                }
            }
        } catch (e) {
            // Keep default fallback badge
        }
    }

    fetchSystemHealth();

    // --- 12. Translation History Management ---
    const historyToggle = document.getElementById("history-toggle");
    const historyToggleIcon = document.getElementById("history-toggle-icon");
    let translationHistory = JSON.parse(localStorage.getItem("polyglot_history") || "[]");
    renderHistory();

    // Collapsible History Drawer Toggle
    if (historyToggle && historyList) {
        historyToggle.addEventListener("click", (e) => {
            // Prevent toggling if user clicked Clear All button
            if (e.target.closest("#btn-clear-history")) return;

            const isCollapsed = historyList.classList.toggle("collapsed");
            historyToggle.setAttribute("aria-expanded", String(!isCollapsed));
            if (historyToggleIcon) {
                historyToggleIcon.style.transform = isCollapsed ? "rotate(-90deg)" : "rotate(0deg)";
            }
        });
    }

    function saveToHistory(entry) {
        entry.id = Date.now();
        translationHistory.unshift(entry);
        if (translationHistory.length > 10) {
            translationHistory = translationHistory.slice(0, 10);
        }
        localStorage.setItem("polyglot_history", JSON.stringify(translationHistory));
        renderHistory();
    }

    function renderHistory() {
        historyCount.textContent = translationHistory.length;
        historyList.innerHTML = "";

        if (translationHistory.length === 0) {
            historyList.innerHTML = `<div class="empty-history-text">No recent translations in this session.</div>`;
            return;
        }

        translationHistory.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";

            const badge = document.createElement("span");
            badge.className = "history-pair-badge";
            badge.textContent = `${item.sourceLang.toUpperCase()} → ${item.targetLang.toUpperCase()}`;

            const preview = document.createElement("span");
            preview.className = "history-text-preview";
            preview.title = item.source;
            preview.textContent = `"${item.source}"`;

            const time = document.createElement("span");
            time.style.fontSize = "0.75rem";
            time.style.color = "var(--text-muted)";
            time.textContent = item.timestamp;

            const btnContainer = document.createElement("div");
            btnContainer.style.display = "flex";
            btnContainer.style.gap = "0.35rem";
            btnContainer.style.alignItems = "center";

            const restoreBtn = document.createElement("button");
            restoreBtn.className = "history-restore-btn";
            restoreBtn.title = "Restore into translation cards";
            restoreBtn.textContent = "Restore";

            const deleteBtn = document.createElement("button");
            deleteBtn.className = "history-delete-btn";
            deleteBtn.title = "Delete this translation";
            deleteBtn.style.background = "transparent";
            deleteBtn.style.border = "none";
            deleteBtn.style.color = "var(--text-muted)";
            deleteBtn.style.cursor = "pointer";
            deleteBtn.style.padding = "0.2rem 0.4rem";
            deleteBtn.style.fontSize = "0.85rem";
            deleteBtn.style.borderRadius = "4px";
            deleteBtn.textContent = "✕";

            btnContainer.appendChild(restoreBtn);
            btnContainer.appendChild(deleteBtn);

            div.appendChild(badge);
            div.appendChild(preview);
            div.appendChild(time);
            div.appendChild(btnContainer);

            // Restore action
            div.querySelector(".history-restore-btn").addEventListener("click", () => {
                sourceText.value = item.source;
                targetText.value = item.target;
                sourceLang.value = item.sourceLang;
                targetLang.value = item.targetLang;
                hasTranslated = true;
                updateCharCounter();
                showStatusBanner("Restored translation from history.", "info", 2000);
            });

            // Delete single item action
            div.querySelector(".history-delete-btn").addEventListener("click", () => {
                translationHistory = translationHistory.filter(h => h.id !== item.id);
                localStorage.setItem("polyglot_history", JSON.stringify(translationHistory));
                renderHistory();
                showStatusBanner("Item removed from history.", "info", 1500);
            });

            historyList.appendChild(div);
        });
    }

    btnClearHistory.addEventListener("click", () => {
        translationHistory = [];
        localStorage.removeItem("polyglot_history");
        renderHistory();
        showStatusBanner("Translation history cleared.", "info", 2000);
    });

    // Preload available SpeechSynthesis voices
    if ("speechSynthesis" in window) {
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }
});
