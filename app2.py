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

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background-color: #ffffff;
    }

    .main .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background-color: #f8fbff;
        border-right: 1px solid #e5edf5;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 700;
        color: #172033;
    }

    .sidebar-description {
        font-size: 0.82rem;
        color: #718096;
        margin-top: 2px;
        margin-bottom: 2rem;
    }

    .sidebar-heading {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
    }

    .sidebar-item {
        background-color: #ffffff;
        border: 1px solid #e5edf5;
        border-radius: 9px;
        padding: 11px 12px;
        margin-bottom: 8px;
    }

    .sidebar-item-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #334155;
    }

    .sidebar-item-description {
        font-size: 0.74rem;
        color: #7b8797;
        margin-top: 3px;
    }


    /* ==============================
       HEADER
    ============================== */

    .app-header {
        margin-bottom: 1.8rem;
    }

    .app-title {
        font-size: 2.15rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #172033;
        margin-bottom: 0.35rem;
    }

    .app-subtitle {
        font-size: 0.96rem;
        color: #718096;
    }


    /* ==============================
       WELCOME
    ============================== */

    .welcome-box {
        text-align: center;
        padding-top: 4rem;
        padding-bottom: 3.5rem;
    }

    .welcome-icon {
        font-size: 2.2rem;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }

    .welcome-title {
        font-size: 1.45rem;
        font-weight: 650;
        color: #273449;
        margin-bottom: 0.45rem;
    }

    .welcome-description {
        max-width: 600px;
        margin: auto;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #7a8797;
    }


    /* ==============================
       CHAT MESSAGES
    ============================== */

    .user-message {
        background-color: #eef6ff;
        border: 1px solid #dcecff;
        border-radius: 14px 14px 4px 14px;
        padding: 12px 16px;
        margin: 12px 0 12px auto;
        max-width: 78%;
        color: #26364d;
    }

    .assistant-message {
        background-color: #fafcff;
        border: 1px solid #e7edf4;
        border-radius: 14px 14px 14px 4px;
        padding: 15px 18px;
        margin: 12px auto 18px 0;
        max-width: 82%;
        color: #293548;
    }

    .message-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #8a98aa;
        margin-bottom: 5px;
    }


    /* ==============================
       CHAT INPUT
    ============================== */

    div[data-testid="stChatInput"] {
        border-top: none !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
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


    /* ==============================
       BUTTON
    ============================== */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #dce5ef;
        background-color: #ffffff;
        color: #536275;
        font-size: 0.82rem;
    }

    .stButton > button:hover {
        border-color: #b8d3f2;
        color: #2563eb;
        background-color: #f5f9ff;
    }


    /* ==============================
       FOOTER
    ============================== */

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
        '<div class="sidebar-brand">TechnoSense</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-description">'
        'AI Knowledge Assistant'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">Knowledge Base</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-item">
            <div class="sidebar-item-title">
                TechnoSense Knowledge Base
            </div>
            <div class="sidebar-item-description">
                Company services, solutions and business information
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">RAG System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-item">
            <div class="sidebar-item-title">
                Semantic Search
            </div>
            <div class="sidebar-item-description">
                OpenSearch vector retrieval
            </div>
        </div>

        <div class="sidebar-item">
            <div class="sidebar-item-title">
                AI Model
            </div>
            <div class="sidebar-item-description">
                Amazon Nova Lite
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-heading">Conversation</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.markdown(
        '<div class="footer">TechnoSense AI Assistant</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">TechnoSense AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Ask questions about TechnoSense services, solutions, '
    'and business information.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE RAG
# ============================================================

@st.cache_resource
def initialize_rag():

    embeddings = create_embeddings()

    client = create_opensearch_client()

    llm = create_llm()

    prompt = create_prompt()

    return embeddings, client, llm, prompt


embeddings, client, llm, prompt = initialize_rag()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="welcome-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-icon">✦</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-title">How can I help you?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-description">'
        'Ask me anything about TechnoSense services, '
        'cloud solutions, infrastructure, development, '
        'databases, Microsoft 365, and other information '
        'available in the knowledge base.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            '<div class="user-message">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="message-label">You</div>',
            unsafe_allow_html=True
        )

        st.write(message["content"])

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="assistant-message">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="message-label">TechnoSense AI</div>',
            unsafe_allow_html=True
        )

        st.write(message["content"])

        st.markdown(
            '</div>',
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

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Display user message
    st.markdown(
        '<div class="user-message">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="message-label">You</div>',
        unsafe_allow_html=True
    )

    st.write(question)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # Generate response
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

        except Exception as e:

            answer = (
                "Sorry, I encountered an error while "
                "processing your question."
            )

            st.error(str(e))

    # Store assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Display assistant response
    st.markdown(
        '<div class="assistant-message">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="message-label">TechnoSense AI</div>',
        unsafe_allow_html=True
    )

    st.write(answer)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

