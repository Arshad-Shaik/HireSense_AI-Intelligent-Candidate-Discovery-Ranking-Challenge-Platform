# ai-service/retrieval/topk_retriever.py

from retrieval.similarity_search import (
    semantic_search
)


def extract_top_candidates(
        query_embedding,
        top_k=1000
):

    results = semantic_search(

        query_embedding,

        top_k

    )

    return results