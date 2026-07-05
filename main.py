from pathlib import Path

from proccess_doc import (
    chunking,
    pdf_to_markdown,
)
from llm_call import generate_response
from prompt_builder import build_final_prompt
from retriever import retrieve_from_vector_db
from vector_db import chunk_in_vector_db


def prompt_for_document_path() -> str | None:
    document_path = input("Enter the document path (PDF) to add, or 'quit' to exit: ").strip()
    if not document_path or document_path.lower() in {"q", "quit", "exit"}:
        return None
    return document_path


def main() -> None:
    print("Document ingestion + RAG demo")

    document_path = None
    while document_path is None:
        document_path = prompt_for_document_path()
        if document_path is None:
            print("No document provided. Exiting.")
            return

    if not Path(document_path).exists():
        print(f"The file '{document_path}' was not found.")
        return

    print("Converting the document to markdown...")
    markdown_object = pdf_to_markdown(document_path)

    print("Chunking the document...")
    chunks = chunking(markdown_object)

    print(f"Indexing {len(chunks)} chunks...")
    chunk_in_vector_db(chunks)

    while True:
        user_query = input("\nEnter your question (or 'quit' to exit): ").strip()
        if not user_query or user_query.lower() in {"q", "quit", "exit"}:
            break

        retrieved_chunks = retrieve_from_vector_db(user_query, top_k=5, alpha=0.5)
        final_prompt = build_final_prompt(user_query, retrieved_chunks=retrieved_chunks)
        print("\n--- FINAL PROMPT ---\n" + final_prompt)

        try:
            response = generate_response(final_prompt)
        except Exception as exc:
            print(f"Unable to generate an LLM response: {exc}")
            continue

        print("\n--- LLM RESPONSE ---\n" + response)


if __name__ == "__main__":
    main()
