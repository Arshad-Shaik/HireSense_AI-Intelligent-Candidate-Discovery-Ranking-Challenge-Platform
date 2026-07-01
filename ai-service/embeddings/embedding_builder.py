# ai-service/embeddings/embedding_builder.py

from embeddings.embedding_model import (
    get_embedding_model,
)


BGE_QUERY_PREFIX: str = (
    "Represent this sentence for searching relevant passages: "
)


def generate_embedding(
    candidate_text: str,
) -> list:
    """
    Generate embedding for CANDIDATE DOCUMENT.

    Used by index_data.py to store in ChromaDB.
    NO prefix applied.

    Args:
        candidate_text: Full candidate profile text

    Returns:
        list: 1024-dim embedding vector
    """
    if not candidate_text or not isinstance(candidate_text, str):
        candidate_text = ""

    model = get_embedding_model()

    embedding = model.encode(
        candidate_text.strip(),
        normalize_embeddings=True,
    )

    return embedding.tolist()


def generate_query_embedding(
    query_text: str,
) -> list:
    """
    Generate embedding for JD QUERY.

    Used by query_embedding.py at rank time.
    MUST apply BGE query prefix.

    Args:
        query_text: Raw job description text

    Returns:
        list: 1024-dim query embedding vector
    """
    if not query_text or not isinstance(query_text, str):
        query_text = ""

    prefixed_text = BGE_QUERY_PREFIX + query_text.strip()

    model = get_embedding_model()

    embedding = model.encode(
        prefixed_text,
        normalize_embeddings=True,
    )

    return embedding.tolist()