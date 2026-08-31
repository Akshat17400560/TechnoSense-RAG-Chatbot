from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
from retriever import (
    create_embeddings,
    create_opensearch_client,
    similarity_search
)


def create_llm():

    return ChatBedrockConverse(
        model_id="amazon.nova-lite-v1:0",
        region_name="us-east-1",
        temperature=0
    )


def build_context(documents):

    context_parts = []

    for document in documents:

        title = document.metadata.get(
            "title",
            "Unknown"
        )

        content = document.page_content

        context_parts.append(
            f"Source: {title}\n{content}"
        )

    return "\n\n".join(context_parts)


def create_prompt():

    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are the TechnoSense knowledge assistant.

                Answer the user's question using only the provided context.

                Do not make up information.

                If the answer cannot be found in the context, say:

                "I could not find this information in the TechnoSense knowledge base."

                Context:

                {context}
                """
            ),
            (
                "human",
                "{question}"
            )
        ]
    )


def ask_technosense(
    question,
    client,
    embeddings,
    llm,
    prompt
):

    documents = similarity_search(
        client=client,
        embeddings=embeddings,
        query=question,
        k=5
    )

    context = build_context(
        documents
    )

    formatted_prompt = prompt.invoke(
        {
            "context": context,
            "question": question
        }
    )

    response = llm.invoke(
        formatted_prompt
    )

    return response.content


def main():

    print("=" * 60)
    print("TechnoSense RAG Assistant")
    print("=" * 60)

    embeddings = create_embeddings()

    client = create_opensearch_client()

    llm = create_llm()

    prompt = create_prompt()

    while True:

        question = input(
            "\nAsk TechnoSense "
            "(type 'exit' to quit): "
        )

        if question.lower() == "exit":
            break

        answer = ask_technosense(
            question=question,
            client=client,
            embeddings=embeddings,
            llm=llm,
            prompt=prompt
        )

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()