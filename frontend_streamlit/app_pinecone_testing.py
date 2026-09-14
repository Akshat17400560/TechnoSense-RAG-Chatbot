import streamlit as st
from datetime import datetime

from rag_pipeline_pinecone import generate_answer


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TechnoSense AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- General layout ---------- */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 820px;
    }

    /* ---------- Header ---------- */
    .hero {
        text-align: center;
        padding: 28px 20px 22px 20px;
        border-radius: 18px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 45%, #a855f7 100%);
        margin-bottom: 28px;
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.25);
    }

    .hero-icon {
        font-size: 42px;
        margin-bottom: 6px;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        font-weight: 400;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 14px;
        padding: 5px 14px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.18);
        color: #ffffff;
        font-size: 12.5px;
        font-weight: 600;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.25);
    }

    /* ---------- Suggested question chips ---------- */
    .chip-row-label {
        font-size: 13px;
        font-weight: 600;
        color: #6b7280;
        margin: 4px 0 10px 2px;
    }

    /* ---------- Chat bubbles ---------- */
    div[data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 4px 6px;
        margin-bottom: 6px;
    }

    /* ---------- Source box ---------- */
    .source-box {
        padding: 12px 14px;
        border-radius: 10px;
        margin-top: 12px;
        background: rgba(99, 102, 241, 0.07);
        border-left: 3px solid #6366f1;
        font-size: 13.5px;
    }

    /* ---------- Footer note ---------- */
    .footer-note {
        text-align: center;
        font-size: 12px;
        color: #9ca3af;
        margin-top: 10px;
    }

    /* ---------- Sidebar ---------- */
    .sidebar-card {
        padding: 14px 16px;
        border-radius: 12px;
        background: rgba(99, 102, 241, 0.07);
        margin-bottom: 14px;
    }

    .sidebar-card h4 {
        margin: 0 0 8px 0;
        font-size: 14px;
    }

    .tech-pill {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px 4px 3px 0;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.12);
        font-size: 12px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🤖</div>
        <div class="hero-title">TechnoSense AI Assistant</div>
        <p class="hero-subtitle">Ask questions about TechnoSense services, solutions and capabilities.</p>
        <div class="status-pill"><span class="status-dot"></span>Knowledge base connected</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 5. SUGGESTED QUESTIONS (shown only before the first message)
# ============================================================

SUGGESTED_QUESTIONS = [
    "What services does TechnoSense offer?",
    "Tell me about your solutions",
    "What industries do you work with?",
    "How can I get started?",
]

if not st.session_state.messages:
    st.markdown('<div class="chip-row-label">✨ Try asking</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    clicked_suggestion = None

    for i, question in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 2]:
            if st.button(question, key=f"suggestion_{i}", use_container_width=True):
                clicked_suggestion = question
else:
    clicked_suggestion = None


# ============================================================
# 6. DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("timestamp"):
            st.caption(message["timestamp"])


# ============================================================
# 7. CHAT INPUT
# ============================================================

user_query = st.chat_input("Ask something about TechnoSense...")

if clicked_suggestion:
    user_query = clicked_suggestion


# ============================================================
# 8. PROCESS USER QUERY
# ============================================================

if user_query:

    now = datetime.now().strftime("%I:%M %p")

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {"role": "user", "content": user_query, "timestamp": now}
    )

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)
        st.caption(now)

    # --------------------------------------------------------
    # Generate assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Searching TechnoSense knowledge base..."):

            try:
                answer = generate_answer(user_query)
                st.markdown(answer)

            except Exception as e:
                answer = (
                    "Sorry, I encountered an error while "
                    "processing your question."
                )
                st.error(answer)
                print(f"Error: {e}")

        reply_time = datetime.now().strftime("%I:%M %p")
        st.caption(reply_time)

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "timestamp": reply_time}
    )

    st.rerun()


# ============================================================
# 9. FOOTER
# ============================================================

if st.session_state.messages:
    st.markdown(
        '<div class="footer-note">Answers are generated from the TechnoSense '
        'knowledge base and may not always be fully accurate.</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 10. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 TechnoSense AI")

    st.markdown(
        """
        <div class="sidebar-card">
            <h4>💡 About</h4>
            This assistant uses Retrieval-Augmented Generation (RAG)
            to answer questions using the TechnoSense knowledge base.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <h4>⚙️ Technology</h4>
            <span class="tech-pill">🧠 Amazon Bedrock</span>
            <span class="tech-pill">🔎 Pinecone</span>
            <span class="tech-pill">📚 Markdown KB</span>
            <span class="tech-pill">🔗 LangChain</span>
            <span class="tech-pill">💬 Streamlit</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-card">
            <h4>❓ How it works</h4>
            Your question is converted into an embedding and searched
            against the TechnoSense knowledge base. The most relevant
            information is then provided to the language model to
            generate a grounded response.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Session", "Active" if st.session_state.messages else "New")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()