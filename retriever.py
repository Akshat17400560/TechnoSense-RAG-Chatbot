import os

from dotenv import load_dotenv
from opensearchpy import (
    OpenSearch,
    RequestsHttpConnection,
    AWSV4SignerAuth
)
from botocore.credentials import Credentials
from langchain_aws import BedrockEmbeddings
from langchain_core.documents import Document


load_dotenv()


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST")
INDEX_NAME = os.getenv(
    "OPENSEARCH_INDEX",
    "technosense-rag"
)


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


def similarity_search(
    client,
    embeddings,
    query,
    k=5
):

    query_vector = embeddings.embed_query(query)

    search_body = {
        "size": k,
        "query": {
            "knn": {
                "vector": {
                    "vector": query_vector,
                    "k": k
                }
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body=search_body
    )

    documents = []

    for hit in response["hits"]["hits"]:

        source = hit["_source"]

        metadata = {
            "document_id": source.get("document_id"),
            "title": source.get("title"),
            "category": source.get("category"),
            "company": source.get("company"),
            "chunk_id": source.get("chunk_id"),
            "total_chunks": source.get("total_chunks"),
            "score": hit.get("_score")
        }

        document = Document(
            page_content=source.get("text", ""),
            metadata=metadata
        )

        documents.append(document)

    return documents


def main():

    print("=" * 60)
    print("TechnoSense RAG Retrieval Test")
    print("=" * 60)

    print("\nInitializing embeddings...")

    embeddings = create_embeddings()

    print("Connecting to OpenSearch...")

    client = create_opensearch_client()

    print("OpenSearch connection established.")

    while True:

        query = input(
            "\nEnter your question "
            "(type 'exit' to quit): "
        )

        if query.lower() == "exit":
            break

        results = similarity_search(
            client=client,
            embeddings=embeddings,
            query=query,
            k=3
        )

        print("\n" + "-" * 60)
        print(f"Retrieved {len(results)} chunks")
        print("-" * 60)

        for i, document in enumerate(results, start=1):

            print(f"\nResult {i}")

            print(
                f"Score: "
                f"{document.metadata.get('score')}"
            )

            print(
                f"Document: "
                f"{document.metadata.get('document_id')}"
            )

            print(
                f"Title: "
                f"{document.metadata.get('title')}"
            )

            print(
                f"Category: "
                f"{document.metadata.get('category')}"
            )

            print(
                f"Chunk: "
                f"{document.metadata.get('chunk_id')}/"
                f"{document.metadata.get('total_chunks')}"
            )

            print("\nContent:")
            print(document.page_content)

    print("\nRetrieval test completed.")


if __name__ == "__main__":
    main()