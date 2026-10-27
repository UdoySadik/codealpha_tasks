/**
 * Supported Languages Catalog and Helper Functions
 * Standard ISO 639-1 Language Code Mapping
 */

const SUPPORTED_LANGUAGES = [
    { code: "en", name: "English", native: "English" },
    { code: "es", name: "Spanish", native: "Español" },
    { code: "fr", name: "French", native: "Français" },
    { code: "de", name: "German", native: "Deutsch" },
    { code: "it", name: "Italian", native: "Italiano" },
    { code: "pt", name: "Portuguese", native: "Português" },
    { code: "ru", name: "Russian", native: "Русский" },
    { code: "zh", name: "Chinese (Simplified)", native: "中文 (简体)" },
    { code: "ja", name: "Japanese", native: "日本語" },
    { code: "ko", name: "Korean", native: "한국어" },
    { code: "ar", name: "Arabic", native: "العربية" },
    { code: "hi", name: "Hindi", native: "हिन्दी" },
    { code: "bn", name: "Bengali", native: "বাংলা" },
    { code: "nl", name: "Dutch", native: "Nederlands" },
    { code: "pl", name: "Polish", native: "Polski" },
    { code: "tr", name: "Turkish", native: "Türkçe" },
    { code: "sv", name: "Swedish", native: "Svenska" },
    { code: "da", name: "Danish", native: "Dansk" },
    { code: "fi", name: "Finnish", native: "Suomi" },
    { code: "no", name: "Norwegian", native: "Norsk" },
    { code: "el", name: "Greek", native: "Ελληνικά" },
    { code: "cs", name: "Czech", native: "Čeština" },
    { code: "ro", name: "Romanian", native: "Română" },
    { code: "hu", name: "Hungarian", native: "Magyar" },
    { code: "uk", name: "Ukrainian", native: "Українська" },
    { code: "vi", name: "Vietnamese", native: "Tiếng Việt" },
    { code: "id", name: "Indonesian", native: "Bahasa Indonesia" },
    { code: "th", name: "Thai", native: "ไทย" },
    { code: "fa", name: "Persian", native: "فارسی" },
    { code: "he", name: "Hebrew", native: "עברית" },
    { code: "ur", name: "Urdu", native: "اردو" },
    { code: "sw", name: "Swahili", native: "Kiswahili" }
];

// Sort alphabetically by English name
SUPPORTED_LANGUAGES.sort((a, b) => a.name.localeCompare(b.name));

/**
 * Populates source and target select elements
 * @param {HTMLSelectElement} sourceSelect 
 * @param {HTMLSelectElement} targetSelect 
 * @param {string} defaultSource 
 * @param {string} defaultTarget 
 */
function populateLanguageSelectors(sourceSelect, targetSelect, defaultSource = "auto", defaultTarget = "es") {
    if (!sourceSelect || !targetSelect) return;

    // Reset options
    sourceSelect.innerHTML = "";
    targetSelect.innerHTML = "";

    // Add Auto-Detect option to source select
    const autoOption = document.createElement("option");
    autoOption.value = "auto";
    autoOption.textContent = "✨ Auto-Detect Language";
    sourceSelect.appendChild(autoOption);

    // Populate languages
    SUPPORTED_LANGUAGES.forEach(lang => {
        // Source option
        const optSource = document.createElement("option");
        optSource.value = lang.code;
        optSource.textContent = `${lang.name} (${lang.native})`;
        sourceSelect.appendChild(optSource);

        // Target option
        const optTarget = document.createElement("option");
        optTarget.value = lang.code;
        optTarget.textContent = `${lang.name} (${lang.native})`;
        targetSelect.appendChild(optTarget);
    });

    sourceSelect.value = defaultSource;
    targetSelect.value = defaultTarget;
}

/**
 * Resolves language code to human-readable name
 * @param {string} code 
 * @returns {string}
 */
function getLanguageName(code) {
    if (code === "auto") return "Auto-Detect";
    const found = SUPPORTED_LANGUAGES.find(l => l.code === code);
    return found ? found.name : code;
}
