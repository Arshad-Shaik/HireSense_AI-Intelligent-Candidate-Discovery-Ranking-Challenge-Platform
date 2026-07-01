# ai-service/embeddings/embedding_model.py

import torch
from sentence_transformers import SentenceTransformer
from config.settings import HF_TOKEN


# ---------------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------------

MODEL_NAME: str = "BAAI/bge-small-en-v1.5"

# ---------------------------------------------------------------------------
# Device Detection
# ---------------------------------------------------------------------------

DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Embedding device: {DEVICE}")
print(f"Embedding model : {MODEL_NAME}")

# ---------------------------------------------------------------------------
# Singleton Model Instance
# ---------------------------------------------------------------------------

_model: SentenceTransformer = SentenceTransformer(
    MODEL_NAME,
    token=HF_TOKEN,
    device=DEVICE,
)


def get_embedding_model() -> SentenceTransformer:
    """
    Return singleton BAAI/bge-small-en-v1.5 model instance.

    Produces 384-dim embeddings.
    Same BGE family as bge-large and bge-base.
    Query prefix required at rank time.
    Device: GPU if available, else CPU.

    Returns:
        SentenceTransformer: loaded model instance
    """
    return _model










# # ai-service/embeddings/embedding_model.py

# At Phase 1 Implemented, we used a different model and the code was commented out.

# from sentence_transformers import SentenceTransformer
# from config.settings import HF_TOKEN


# MODEL_NAME = "all-MiniLM-L6-v2"   # At first used this model


# _model = SentenceTransformer(MODEL_NAME, token=HF_TOKEN)


# def get_embedding_model():
#     return _model