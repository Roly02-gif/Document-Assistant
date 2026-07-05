import weaviate
from typing import Any, Dict, List
import os

def retrieve_from_vector_db(query: str, top_k: int = 5, alpha: float = 0.5) -> List[Dict[str, Any]]:
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

    if weaviate_url and weaviate_api_key:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=weaviate_api_key,
        )
        try:
            response = client.collections.get("Document").query.hybrid(
                query=query,
                limit=top_k,
                alpha=alpha,
            )
            return [obj.properties for obj in response.objects]
        finally:
            client.close()
