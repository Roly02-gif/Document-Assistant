from typing import Any, Dict, List, Optional

from retriever import retrieve_from_vector_db
def build_final_prompt(
    query: str,
    retrieved_chunks: Optional[List[Dict[str, Any]]] = None,
    top_k: int = 5,
    alpha: float = 0.5,
) -> str:
    if retrieved_chunks is None:
        retrieved_chunks = retrieve_from_vector_db(query, top_k=top_k, alpha=alpha)

    context = "\n\n".join(
        [
            f"Section: {chunk.get('section', '')}\nContent: {chunk.get('content', '')}"
            for chunk in retrieved_chunks
        ]
    )

    return (
        "Answer the user query below. Rely on the provided context and be concise.\n\n"
        f"Context:\n{context}\n\nQuery: {query}"
    )