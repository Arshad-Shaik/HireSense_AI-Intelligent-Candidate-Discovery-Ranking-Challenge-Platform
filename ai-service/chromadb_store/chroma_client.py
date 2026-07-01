# ai-service/chromadb_store/chroma_client.py

import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)


def get_chroma_client():

    return client