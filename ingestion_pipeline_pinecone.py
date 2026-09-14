import os
import yaml

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_aws import BedrockEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore

load_dotenv()


# 1. CONFIGURATION


KNOWLEDGE_BASE_DIR = "D:/TechnoSense RAG Chatbot"

INDEX_NAME = os.environ["INDEX_NAME"]


# 2. READ MARKDOWN FILE + EXTRACT YAML FRONT MATTER

def load_markdown_file(file_path):
    """
    Read a Markdown file, extract YAML front matter,
    and return the Markdown content + metadata.

    Expected format:

    ---
    document_id: enterprise_mobility
    title: Enterprise Mobility
    category: IT services
    company: TechnoSense NextGen Solutions Pvt Limited
    ---

    # Enterprise Mobility

    Content...
    """

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    metadata = {}

    # --------------------------------------------------------
    # Check for YAML front matter
    # --------------------------------------------------------

    if content.startswith("---"):

        parts = content.split("---", 2)

        if len(parts) == 3:

            yaml_content = parts[1]
            markdown_content = parts[2].strip()

            try:

                parsed_metadata = yaml.safe_load(yaml_content)

                if parsed_metadata:
                    metadata = parsed_metadata

            except yaml.YAMLError as e:

                print(f"WARNING: Invalid YAML metadata in:")
                print(f"  {file_path}")
                print(f"  Error: {e}")

                markdown_content = content

        else:

            markdown_content = content

    else:

        markdown_content = content

    return markdown_content, metadata



# 3. FIND ALL MARKDOWN FILES

print("========================================")
print("Searching for Markdown documents...")
print("========================================")

md_files = []

for root, dirs, files in os.walk(KNOWLEDGE_BASE_DIR):

    for file in files:

        if file.lower().endswith(".md"):

            file_path = os.path.join(root, file)

            md_files.append(file_path)


print(f"Found {len(md_files)} Markdown documents.\n")



# 4. LOAD ALL MARKDOWN DOCUMENTS

documents = []

print("========================================")
print("Loading documents...")
print("========================================")

for file_path in md_files:

    print(f"Loading: {file_path}")

    # --------------------------------------------------------
    # Read Markdown + extract YAML metadata
    # --------------------------------------------------------

    markdown_content, metadata = load_markdown_file(file_path)

    # --------------------------------------------------------
    # Add additional source metadata
    # --------------------------------------------------------

    relative_path = os.path.relpath(
        file_path,
        KNOWLEDGE_BASE_DIR
    )

    metadata["source_file"] = relative_path
    metadata["file_name"] = os.path.basename(file_path)

    # --------------------------------------------------------
    # Create LangChain Document
    # --------------------------------------------------------

    document = Document(
        page_content=markdown_content,
        metadata=metadata
    )

    documents.append(document)


print(f"\nTotal documents loaded: {len(documents)}")


# 5. DISPLAY DOCUMENT METADATA

print("\n========================================")
print("Checking document metadata...")
print("========================================")

if documents:

    print("\nFirst document:")
    print("----------------------------------------")

    print(documents[0].page_content[:500])

    print("\nMetadata:")
    print("----------------------------------------")

    for key, value in documents[0].metadata.items():

        print(f"{key}: {value}")



# 6. SPLIT DOCUMENTS INTO CHUNKS

print("\n========================================")
print("Splitting documents...")
print("========================================")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=500
)

texts = text_splitter.split_documents(documents)


print(f"Created {len(texts)} chunks.")


# 8. INITIALIZE BEDROCK EMBEDDINGS

print("\n========================================")
print("Initializing Bedrock embeddings...")
print("========================================")

embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1"
)



# 9. STORE CHUNKS + METADATA IN PINECONE

print("\n========================================")
print("Initializing Pinecone vector store...")
print("========================================")

PineconeVectorStore.from_documents(
    documents=texts,
    embedding=embeddings,
    index_name=INDEX_NAME
)


# 10. COMPLETED

print("\n========================================")
print("Ingestion completed successfully!")
print("========================================")

print(f"Documents processed : {len(documents)}")
print(f"Chunks created      : {len(texts)}")
print(f"Pinecone index      : {INDEX_NAME}")