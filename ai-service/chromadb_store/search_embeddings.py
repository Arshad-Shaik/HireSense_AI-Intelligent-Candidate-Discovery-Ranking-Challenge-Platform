# ai-service/chromadb_store/search_embeddings.py

from chromadb_store.candidate_collection import (
    get_candidate_collection
)


def search_candidates(
        query_embedding,
        top_k=5
):

    collection = get_candidate_collection()

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k
    )

    return results