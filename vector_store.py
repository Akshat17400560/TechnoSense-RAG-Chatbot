import os
from dotenv import load_dotenv
from opensearchpy import (
    OpenSearch,
    RequestsHttpConnection,
    AWSV4SignerAuth
)
from botocore.credentials import Credentials
from langchain_aws import BedrockEmbeddings

from ingestion_test import run_ingestion


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST")
INDEX_NAME = os.getenv("OPENSEARCH_INDEX", "technosense-rag")


def create_embeddings():
    return BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        region_name=AWS_REGION
    )


def create_opensearch_client():

    credentials = Credentials(
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY
    )

    auth = AWSV4SignerAuth(
        credentials,
        AWS_REGION,
        "aoss"
    )

    client = OpenSearch(
        hosts=[
            {
                "host": OPENSEARCH_HOST,
                "port": 443
            }
        ],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=60,
        max_retries=3,
        retry_on_timeout=True
    )

    return client


def create_index(client, vector_dimension):

    if client.indices.exists(index=INDEX_NAME):
        print(f"Index already exists: {INDEX_NAME}")
        return

    index_body = {
        "settings": {
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {
                "vector": {
                    "type": "knn_vector",
                    "dimension": vector_dimension,
                    "method": {
                        "name": "hnsw",
                        "space_type": "l2"
                    }
                },
                "text": {
                    "type": "text"
                },
                "document_id": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "category": {
                    "type": "keyword"
                },
                "company": {
                    "type": "keyword"
                },
                "chunk_id": {
                    "type": "integer"
                },
                "total_chunks": {
                    "type": "integer"
                }
            }
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        body=index_body
    )

    print(f"Created index: {INDEX_NAME}")


def upload_chunks(client, chunks, embeddings):

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    print(
        f"Generating embeddings for {len(texts)} chunks..."
    )

    vectors = embeddings.embed_documents(texts)

    print("Embeddings generated successfully.")

    bulk_operations = []

    for chunk, vector in zip(chunks, vectors):

        metadata = chunk.metadata

        document_id = metadata.get(
            "document_id",
            "unknown_document"
        )

        chunk_id = metadata.get(
            "chunk_id",
            0
        )

        record_id = f"{document_id}_{chunk_id}"

        document = {
            "vector": vector,
            "text": chunk.page_content,
            "document_id": metadata.get("document_id"),
            "title": metadata.get("title"),
            "category": metadata.get("category"),
            "company": metadata.get("company"),
            "chunk_id": chunk_id,
            "total_chunks": metadata.get("total_chunks")
        }

        bulk_operations.append(
            {
                "index": {
                    "_index": INDEX_NAME,
                    "_id": record_id
                }
            }
        )

        bulk_operations.append(document)

    print(
        f"Uploading {len(chunks)} chunks to OpenSearch..."
    )

    response = client.bulk(
        body=bulk_operations
    )

    if response.get("errors"):

        failed_documents = []

        for item in response["items"]:

            result = item.get("index", {})

            if result.get("status", 200) >= 300:
                failed_documents.append(result)

        print(
            f"Failed documents: {len(failed_documents)}"
        )

        for failure in failed_documents[:5]:
            print(failure)

        raise RuntimeError(
            "Some documents failed during bulk upload."
        )

    print(
        f"Successfully uploaded {len(chunks)} chunks."
    )


def main():

    print("=" * 60)
    print("TechnoSense RAG Vector Store Pipeline")
    print("=" * 60)

    print("\nLoading and chunking documents...")

    chunks = run_ingestion()

    if not chunks:
        print("No chunks found.")
        return

    print("\nInitializing Bedrock embeddings...")

    embeddings = create_embeddings()

    test_vector = embeddings.embed_query(
        "Test embedding"
    )

    vector_dimension = len(test_vector)

    print(
        f"Embedding dimension: {vector_dimension}"
    )

    print(
        "\nConnecting to OpenSearch Serverless..."
    )

    client = create_opensearch_client()

    print(
        "OpenSearch connection established."
    )

    create_index(
        client,
        vector_dimension
    )

    print("\nUploading chunks...")

    upload_chunks(
        client,
        chunks,
        embeddings
    )

    print("\n" + "=" * 60)
    print(
        "Vector ingestion completed successfully."
    )
    print("=" * 60)


if __name__ == "__main__":
    main()