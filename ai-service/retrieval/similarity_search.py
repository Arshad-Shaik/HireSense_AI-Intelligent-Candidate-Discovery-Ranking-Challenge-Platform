# ai-service/retrieval/similarity_search.py

from chromadb_store.candidate_collection import (
    get_candidate_collection
)


def semantic_search(
        query_embedding,
        top_k=30000
):

    collection = get_candidate_collection()

    results = collection.query(

        query_embeddings=[
            query_embedding
        ],

        n_results=top_k,

        include=[
            "distances",
            "metadatas"
        ]

    )

    return results