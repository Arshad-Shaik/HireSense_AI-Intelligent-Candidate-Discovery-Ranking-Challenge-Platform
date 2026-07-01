# ai-service/chromadb_store/candidate_collection.py

from chromadb_store.chroma_client import (
    get_chroma_client
)


COLLECTION_NAME = "candidates"


def get_candidate_collection():

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection