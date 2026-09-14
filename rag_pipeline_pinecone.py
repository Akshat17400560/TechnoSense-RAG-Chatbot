import os
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings, ChatBedrock
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# 1. CONFIGURATION

INDEX_NAME = os.environ["INDEX_NAME"]

REGION_NAME = "us-east-1"

EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"

LLM_MODEL = "amazon.nova-lite-v1:0"

TOP_K = 5


# 2. INITIALIZE EMBEDDINGS

embeddings = BedrockEmbeddings(
    model_id=EMBEDDING_MODEL,
    region_name=REGION_NAME
)


# 3. CONNECT TO PINECONE

vector_store = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)


# 4. INITIALIZE BEDROCK LLM

llm = ChatBedrock(
    model_id=LLM_MODEL,
    region_name=REGION_NAME,
    model_kwargs={
        "temperature": 0.2
    }
)


# 5. RETRIEVE RELEVANT DOCUMENTS

def retrieve_documents(query):

    results = vector_store.similarity_search_with_score(
        query,
        k=TOP_K
    )

    return results



# 6. BUILD CONTEXT FROM RETRIEVED DOCUMENTS

def build_context(results):

    context_parts = []

    for i, (document, score) in enumerate(results, start=1):

        metadata = document.metadata

        title = metadata.get(
            "title",
            "Unknown"
        )

        category = metadata.get(
            "category",
            "Unknown"
        )

        document_id = metadata.get(
            "document_id",
            "Unknown"
        )

        source_file = metadata.get(
            "source_file",
            "Unknown"
        )

        content = document.page_content

        context = f"""
        SOURCE {i}

        Title: {title}
        Category: {category}
        Document ID: {document_id}
        Source File: {source_file}

        Content:
        {content}
        """

        context_parts.append(context)

    return "\n\n".join(context_parts)



# 7. CREATE RAG PROMPT

def create_prompt(query, context):

    prompt = f"""
    You are the TechnoSense AI Assistant answer the user query like a production grade chatbot.

    Your task is to answer the user's question using ONLY
    the information provided in the CONTEXT below.

    Don't ever mention refer to so and so document at the end of generated answer. 

    IMPORTANT RULES:

    1. Do not use outside knowledge.
    2. Do not make up or hallucinate information.
    3. If the answer cannot be found in the context, clearly say:
        "I don't have enough information in my knowledge base to answer that."
    4. Keep the answer concise, accurate and relevant to the question.
    5. Do not mention the internal retrieval process.
    6. When appropriate, organize the answer using bullet points.
    7. Do not unnecessarily repeat the same information.
    8. Use the source information to understand where the answer came from.
    9. Most importantly don't mention to user that for more information refer to so and so document at the end of response.

    
    ==================================================
    USER QUESTION
    ==================================================
    
    {query}


    ==================================================
    CONTEXT
    ==================================================

    {context}

    """

    return prompt



# 8. GENERATE ANSWER

def generate_answer(query):

    results = retrieve_documents(query)

    if not results:

        return (
            "I don't have enough information in my "
            "knowledge base to answer that."
        )



    # Build context

    context = build_context(results)

    # Create prompt

    prompt = create_prompt(
        query,
        context
    )

    
    # Send prompt to Bedrock

    print("Generating answer...")

    response = llm.invoke(prompt)

    return response.content


