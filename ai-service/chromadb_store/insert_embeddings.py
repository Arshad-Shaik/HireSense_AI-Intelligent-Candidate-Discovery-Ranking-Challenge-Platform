# ai-service/chromadb_store/insert_embeddings.py

from chromadb_store.candidate_collection import (
    get_candidate_collection
)


def insert_candidate_embedding(
        record
):

    collection = get_candidate_collection()

    collection.upsert(

        ids=[
            record["candidate_id"]
        ],

        documents=[
            record["document"]
        ],

        embeddings=[
            record["embedding"]
        ],

        metadatas=[
            record["metadata"]
        ]

    )