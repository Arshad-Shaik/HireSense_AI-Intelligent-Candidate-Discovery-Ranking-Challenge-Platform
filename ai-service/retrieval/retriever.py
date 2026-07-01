# ai-service/retrieval/retriever.py

from retrieval.query_embedding import (
    build_query_embedding
)

from retrieval.topk_retriever import (
    extract_top_candidates
)


def retrieve_top_candidates(
        query_text,
        top_k=1000
):

    query_embedding = build_query_embedding(
        query_text
    )

    results = extract_top_candidates(

        query_embedding,

        top_k

    )

    return results