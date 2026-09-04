import streamlit as st

from rag_pipeline_pinecone import generate_answer


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TechnoSense AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .source-box {
        padding: 12px;
        border-radius: 8px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 TechnoSense AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about TechnoSense services, solutions and capabilities.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 4. INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# 5. DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# 6. CHAT INPUT
# ============================================================

user_query = st.chat_input(
    "Ask something about TechnoSense..."
)


# ============================================================
# 7. PROCESS USER QUERY
# ============================================================

if user_query:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):

        st.markdown(user_query)

    # --------------------------------------------------------
    # Generate assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

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

    # --------------------------------------------------------
    # Save assistant response
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# 8. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("TechnoSense AI")

    st.markdown(
        """
        ### About

        This assistant uses Retrieval-Augmented Generation (RAG)
        to answer questions using the TechnoSense knowledge base.

        ### Technology

        - 🧠 Amazon Bedrock
        - 🔎 Pinecone Vector Database
        - 📚 Markdown Knowledge Base
        - 🔗 LangChain
        - 💬 Streamlit

        ### How it works

        Your question is converted into an embedding and searched
        against the TechnoSense knowledge base.

        The most relevant information is then provided to the
        language model to generate a grounded response.
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()