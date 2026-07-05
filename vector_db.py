import weaviate
from weaviate.classes.config import Configure
import os
from typing import Any, Dict, List


def chunk_in_vector_db(chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

    if weaviate_url and weaviate_api_key:
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=weaviate_api_key,
        )

        try:
            if not client.collections.exists("Document"):
                client.collections.create(
                    name="Document",
                    vector_config=Configure.Vectors.text2vec_weaviate(),
                )

            document = client.collections.use("Document")
            with document.batch.fixed_size(batch_size=200) as batch:
                for obj in chunks:
                    batch.add_object(properties=obj)
        finally:
            client.close()

        print(f"Imported {len(chunks)} chunks into the Weaviate collection")
        return {"source": "weaviate", "count": len(chunks)}

    return {"source": "local_file", "count": len(chunks)}
