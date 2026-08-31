from pathlib import Path
import yaml
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


KNOWLEDGE_BASE = Path("D:\RAG_Chatbot_Technosense_BACKUP")


def parse_markdown_file(file_path):
    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        raise ValueError(f"No YAML frontmatter found in: {file_path}")

    parts = content.split("---", 2)

    if len(parts) != 3:
        raise ValueError(f"Invalid YAML frontmatter format in: {file_path}")

    metadata = yaml.safe_load(parts[1]) or {}
    document_text = parts[2].strip()

    if not isinstance(metadata, dict):
        raise ValueError(f"Metadata must be a YAML dictionary in: {file_path}")

    return metadata, document_text


def load_documents():
    documents = []

    for file_path in KNOWLEDGE_BASE.rglob("*.md"):
        try:
            metadata, content = parse_markdown_file(file_path)

            documents.append(
                Document(
                    page_content=content,
                    metadata=metadata
                )
            )

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return documents


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=500
    )

    chunked_documents = []

    for document in documents:
        chunks = splitter.split_text(document.page_content)
        total_chunks = len(chunks)

        for chunk_id, chunk in enumerate(chunks):
            chunked_documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        **document.metadata,
                        "chunk_id": chunk_id,
                        "total_chunks": total_chunks
                    }
                )
            )

    return chunked_documents


def run_ingestion():
    documents = load_documents()
    print(f"Documents loaded: {len(documents)}")

    chunks = chunk_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    # for i, document in enumerate(chunks[:10]):
    #     print(f"\nChunk {i + 1}")
    #     print("-" * 60)
    #     print(document.page_content)
    #     print("\nMetadata:")
    #     print(document.metadata)

    return chunks


if __name__ == "__main__":
    chunks = run_ingestion()
