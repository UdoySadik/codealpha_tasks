"""
app.py
Intelligent Campus Services FAQ Chatbot — Streamlit Web Application.

Interactive, responsive conversational interface built with Streamlit, scikit-learn,
and NLTK vector-space retrieval engine.
"""

from __future__ import annotations

import datetime
from typing import Optional
import streamlit as st

from src.config import DEFAULT_CONFIG, AppConfig
from src.knowledge_base import FAQKnowledgeBase
from src.matcher import FAQMatcher, MatchResult
from src.preprocessor import DEFAULT_PREPROCESSOR

# ==============================================================================
# Page Configuration & Styling
# ==============================================================================
st.set_page_config(
    page_title="Campus Services FAQ Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for enhanced micro-animations, typography, and badges
CUSTOM_CSS = """
<style>
    /* Global Container Adjustments */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 950px;
    }

    /* Welcome Hero Card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(79, 70, 229, 0.3);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .welcome-title {
        font-size: 1.45rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
    }
    .welcome-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        line-height: 1.5;
        margin-bottom: 16px;
    }

    /* Accessibility & Focus Outlines */
    :focus-visible {
        outline: 2px solid #6366F1 !important;
        outline-offset: 2px !important;
    }
    html {
        scroll-behavior: smooth;
    }

    /* Meta Badges */
    .meta-tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.80rem;
        font-weight: 600;
        margin-right: 8px;
        margin-top: 6px;
        letter-spacing: 0.01em;
    }
    .meta-match {
        background-color: rgba(16, 185, 129, 0.18);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .meta-fallback {
        background-color: rgba(245, 158, 11, 0.18);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .meta-category {
        background-color: rgba(99, 102, 241, 0.18);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.4);
    }

    /* Suggestion Chips */
    div[data-testid="stHorizontalBlock"] button {
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(99, 102, 241, 0.4);
        background-color: rgba(30, 41, 59, 0.7);
        color: #F8FAFC;
        padding: 8px 14px;
        transition: all 0.22s ease-in-out;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        background-color: #4F46E5 !important;
        border-color: #6366F1 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
    }

    /* Chat Messages Card Styling */
    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 12px;
        line-height: 1.6;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# Engine Initialization & Caching
# ==============================================================================
@st.cache_resource(show_spinner="Initializing FAQ Retrieval Engine...")
def load_faq_matcher(config_data_path: str) -> tuple[Optional[FAQMatcher], Optional[str]]:
    """
    Load knowledge base and fit TF-IDF vectorizer once per session.
    """
    try:
        kb = FAQKnowledgeBase(config_data_path)
        kb.load()
        matcher = FAQMatcher(
            knowledge_base=kb,
            preprocessor=DEFAULT_PREPROCESSOR,
            config=DEFAULT_CONFIG,
        )
        matcher.fit()
        return matcher, None
    except Exception as exc:
        return None, str(exc)


# ==============================================================================
# Session State Setup
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ==============================================================================
# Header & Branding
# ==============================================================================
col_title, col_status = st.columns([0.8, 0.2])
with col_title:
    st.title("🎓 Campus Services FAQ Assistant")
    st.caption("Ask questions about course registration, tuition, ID cards, library access, and campus IT.")
with col_status:
    st.markdown(
        "<div style='text-align: right; padding-top: 20px;'>"
        "<span class='meta-tag meta-match'>● Local Engine Online</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# Load Matcher
matcher, load_error = load_faq_matcher(str(DEFAULT_CONFIG.faq_data_path))

if load_error or matcher is None:
    st.error(f"⚠️ Error loading FAQ knowledge base: {load_error}")
    st.stop()


# ==============================================================================
# Sidebar: Knowledge Base Stats & Engine Controls
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Chatbot Settings")

    st.markdown("### 📚 Knowledge Base Metrics")
    st.metric("Curated FAQ Topics", matcher.kb.count_faqs())
    st.metric("Indexed Question Patterns", matcher.kb.count_patterns())

    with st.expander("📂 View Categories", expanded=False):
        for cat in matcher.kb.get_all_categories():
            st.markdown(f"- **{cat}**")

    st.divider()

    st.markdown("### 🎛️ Matching Engine Tuning")
    threshold = st.slider(
        "Similarity Threshold (τ)",
        min_value=0.10,
        max_value=0.80,
        value=float(DEFAULT_CONFIG.similarity_threshold),
        step=0.05,
        help="Minimum cosine similarity required to accept a question match. Lower values increase recall; higher values increase precision.",
    )

    show_confidence = st.toggle(
        "Show Match Confidence & Metadata",
        value=True,
        help="Displays the raw cosine similarity score and category badge under each answer.",
    )

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_query = None
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<div style='font-size: 0.8rem; color: #64748B; text-align: center;'>"
        "CodeAlpha AI Internship — Task 2<br>"
        "Zero API Dependencies | 100% Local NLP"
        "</div>",
        unsafe_allow_html=True,
    )


# ==============================================================================
# Main Chat Area: Empty State & Suggested Chips
# ==============================================================================
SUGGESTED_PROMPTS = [
    "How do I register for semester courses?",
    "Where can I pay my tuition fees?",
    "Where can I get my student ID card?",
    "How do I connect to campus Wi-Fi?",
]

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-title">👋 Welcome to Student Campus Services!</div>
            <div class="welcome-subtitle">
                I can help answer questions regarding course registration, fee payments, student ID cards, 
                library loan policies, and IT assistance. Select a suggested topic below or type your own question.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**💡 Quick Suggestions:**")
    cols = st.columns(len(SUGGESTED_PROMPTS))
    for i, prompt in enumerate(SUGGESTED_PROMPTS):
        with cols[i]:
            if st.button(prompt, key=f"chip_{i}", use_container_width=True):
                st.session_state.pending_query = prompt
                st.rerun()


# ==============================================================================
# Render Conversation Timeline
# ==============================================================================
for msg in st.session_state.messages:
    role = msg["role"]
    avatar = "🧑‍🎓" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

        # Display metadata tags for assistant messages if enabled
        if role == "assistant" and show_confidence and "score" in msg:
            status = msg.get("status", "")
            score = msg.get("score", 0.0)
            category = msg.get("category")
            timestamp = msg.get("timestamp", "")

            badge_html = "<div style='margin-top: 8px;'>"
            if status == "MATCH_FOUND":
                badge_html += f"<span class='meta-tag meta-match'>🎯 Similarity: {score:.2f}</span>"
            elif status == "FALLBACK":
                badge_html += f"<span class='meta-tag meta-fallback'>🔍 Fallback (Score: {score:.2f} &lt; {threshold:.2f})</span>"
            elif status == "EMPTY_QUERY":
                badge_html += "<span class='meta-tag meta-fallback'>⚠️ Empty Input</span>"

            if category:
                badge_html += f"<span class='meta-tag meta-category'>🏷️ {category}</span>"

            if timestamp:
                badge_html += f"<span style='color: #64748B; font-size: 0.75rem;'>🕒 {timestamp}</span>"

            badge_html += "</div>"
            st.markdown(badge_html, unsafe_allow_html=True)


# ==============================================================================
# Process User Submission (Chat Input or Clicked Chip)
# ==============================================================================
user_input = st.chat_input("Ask a question about campus services, tuition, or registration...")

active_query = None
if st.session_state.pending_query:
    active_query = st.session_state.pending_query
    st.session_state.pending_query = None
elif user_input:
    active_query = user_input

if active_query:
    now_str = datetime.datetime.now().strftime("%I:%M %p")

    # Record user message
    st.session_state.messages.append({
        "role": "user",
        "content": active_query,
        "timestamp": now_str,
    })

    # Evaluate query through the NLP matcher engine
    match_result: MatchResult = matcher.match(active_query, threshold_override=threshold)

    category_label = match_result.matched_faq.category if match_result.matched_faq else None
    faq_id_label = match_result.matched_faq.id if match_result.matched_faq else None

    # Record assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": match_result.answer,
        "score": match_result.confidence_score,
        "status": match_result.status,
        "category": category_label,
        "faq_id": faq_id_label,
        "timestamp": now_str,
    })

    st.rerun()
