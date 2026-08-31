import streamlit as st

from rag_chain import (
    create_embeddings,
    create_opensearch_client,
    create_llm,
    create_prompt,
    ask_technosense
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TechnoSense AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       Global
    ------------------------------------------------------- */

    .stApp {
        background: #ffffff;
    }

    .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }


    /* -------------------------------------------------------
       Sidebar
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: #f8fbff;
        border-right: 1px solid #e6eef7;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
    }

    .sidebar-logo {
        font-size: 1.35rem;
        font-weight: 700;
        color: #172033;
        margin-bottom: 0.15rem;
    }

    .sidebar-subtitle {
        font-size: 0.82rem;
        color: #718096;
        margin-bottom: 2rem;
    }

    .sidebar-section {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #8a98aa;
        margin-top: 1.4rem;
        margin-bottom: 0.65rem;
    }

    .sidebar-info {
        background: #ffffff;
        border: 1px solid #e5edf6;
        border-radius: 10px;
        padding: 12px 13px;
        margin-bottom: 8px;
    }

    .sidebar-info-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
    }

    .sidebar-info-text {
        font-size: 0.75rem;
        color: #7b8797;
        margin-top: 3px;
    }


    /* -------------------------------------------------------
       Header
    ------------------------------------------------------- */

    .header-container {
        margin-bottom: 2rem;
    }

    .header-title {
        font-size: 2.15rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #172033;
        margin-bottom: 0.35rem;
    }

    .header-subtitle {
        font-size: 0.98rem;
        color: #718096;
        line-height: 1.6;
    }


    /* -------------------------------------------------------
       Welcome Screen
    ------------------------------------------------------- */

    .welcome-container {
        text-align: center;
        padding: 4.5rem 1rem 3rem 1rem;
    }

    .welcome-icon {
        font-size: 2.4rem;
        color: #3b82f6;
        margin-bottom: 0.7rem;
    }

    .welcome-title {
        font-size: 1.45rem;
        font-weight: 650;
        color: #273449;
        margin-bottom: 0.5rem;
    }

    .welcome-text {
        font-size: 0.92rem;
        color: #7a8797;
        max-width: 560px;
        margin: auto;
        line-height: 1.6;
    }


    /* -------------------------------------------------------
       Chat Messages
    ------------------------------------------------------- */

    .user-message-wrapper {
        display: flex;
        justify-content: flex-end;
        margin: 1.1rem 0;
    }

    .user-message {
        max-width: 78%;
        background: #eef6ff;
        border: 1px solid #dcecff;
        border-radius: 15px 15px 4px 15px;
        padding: 12px 16px;
        color: #26364d;
        font-size: 0.94rem;
        line-height: 1.55;
    }

    .assistant-message-wrapper {
        display: flex;
        justify-content: flex-start;
        margin: 1.1rem 0 1.5rem 0;
    }

    .assistant-message {
        max-width: 82%;
        background: #fafcff;
        border: 1px solid #e8edf4;
        border-radius: 15px 15px 15px 4px;
        padding: 15px 18px;
        color: #293548;
        font-size: 0.94rem;
        line-height: 1.65;
    }

    .message-label {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #8a98aa;
        margin-bottom: 5px;
    }


    /* -------------------------------------------------------
       Chat Input
    ------------------------------------------------------- */

    div[data-testid="stChatInput"] {
        border-top: none !important;
    }

    div[data-testid="stChatInput"] > div {
        background: #ffffff !important;
        border: 1px solid #dce5ef !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 18px rgba(31, 55, 80, 0.06) !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #26364d !important;
        font-size: 0.94rem !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #9aa7b5 !important;
    }


    /* -------------------------------------------------------
       Buttons
    ------------------------------------------------------- */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #dce5ef;
        background: #ffffff;
        color: #536275;
        font-size: 0.82rem;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #b8d3f2;
        color: #2563eb;
        background: #f5f9ff;
    }


    /* -------------------------------------------------------
       Divider
    ------------------------------------------------------- */

    .soft-divider {
        height: 1px;
        background: #edf1f5;
        margin: 1.5rem 0;
    }


    /* -------------------------------------------------------
       Footer
    ------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #a0aab7;
        font-size: 0.72rem;
        margin-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">TechnoSense</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'AI Knowledge Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Knowledge Base</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-info">
            <div class="sidebar-info-title">
                TechnoSense Knowledge Base
            </div>
            <div class="sidebar-info-text">
                Company services, solutions and business information
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">RAG System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-info">
            <div class="sidebar-info-title">
                Semantic Search
            </div>
            <div class="sidebar-info-text">
                OpenSearch vector retrieval
            </div>
        </div>

        <div class="sidebar-info">
            <div class="sidebar-info-title">
                AI Model
            </div>
            <div class="sidebar-info-text">
                Amazon Nova Lite
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Conversation</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown(
        """
        <div class="footer">
            TechnoSense AI Assistant
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="header-container">

        <div class="header-title">
            TechnoSense AI Assistant
        </div>

        <div class="header-subtitle">
            Ask questions about TechnoSense services,
            solutions, and business information.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE RAG COMPONENTS
# ============================================================

@st.cache_resource
def initialize_rag():

    embeddings = create_embeddings()

    client = create_opensearch_client()

    llm = create_llm()

    prompt = create_prompt()

    return (
        embeddings,
        client,
        llm,
        prompt
    )


embeddings, client, llm, prompt = initialize_rag()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# WELCOME SCREEN
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-container">

            <div class="welcome-icon">
                ✦
            </div>

            <div class="welcome-title">
                How can I help you?
            </div>

            <div class="welcome-text">
                Ask me anything about TechnoSense services,
                cloud solutions, infrastructure, development,
                databases, Microsoft 365, and other information
                available in the knowledge base.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message-wrapper">

                <div class="user-message">

                    <div class="message-label">
                        You
                    </div>

                    {message["content"]}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-message-wrapper">

                <div class="assistant-message">

                    <div class="message-label">
                        TechnoSense AI
                    </div>

                    {message["content"]}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about TechnoSense..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.markdown(
        f"""
        <div class="user-message-wrapper">

            <div class="user-message">

                <div class="message-label">
                    You
                </div>

                {question}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    with st.spinner(
        "Searching the TechnoSense knowledge base..."
    ):

        try:

            answer = ask_technosense(
                question=question,
                client=client,
                embeddings=embeddings,
                llm=llm,
                prompt=prompt
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            answer = (
                "Sorry, I encountered an error while "
                "processing your question."
            )

            st.error(str(e))

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    st.markdown(
        f"""
        <div class="assistant-message-wrapper">

            <div class="assistant-message">

                <div class="message-label">
                    TechnoSense AI
                </div>

                {answer}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )