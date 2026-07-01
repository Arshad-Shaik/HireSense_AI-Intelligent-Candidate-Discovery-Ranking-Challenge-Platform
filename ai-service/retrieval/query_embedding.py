# ai-service/retrieval/query_embedding.py

from embeddings.embedding_builder import (
    generate_query_embedding,
)


def build_query_embedding(
    job_description: str,
) -> list:
    """
    Build BGE query embedding for job description.

    Applies required BGE query prefix before encoding.

    Args:
        job_description: Raw JD text

    Returns:
        list: 1024-dim query embedding vector
    """
    if not job_description or not job_description.strip():
        raise ValueError(
            "Job description is empty. "
            "Cannot build query embedding."
        )

    return generate_query_embedding(job_description)