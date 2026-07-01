# ai-service/indexing/bulk_indexer.py

from embeddings.candidate_embedding import (
    build_candidate_text
)

from embeddings.embedding_builder import (
    generate_embedding
)

from embeddings.embedding_store import (
    prepare_embedding_record
)

from chromadb_store.insert_embeddings import (
    insert_candidate_embedding
)


def index_candidates(
        candidates
):
    """
    Index ALL candidates into ChromaDB.

    Domain filtering is performed later
    during semantic ranking, not here.
    """

    total = len(candidates)

    print(
        f"\nStarting indexing of {total} candidates...\n"
    )

    for idx, candidate in enumerate(

            candidates,

            start=1

    ):

        candidate_text = build_candidate_text(
            candidate
        )

        embedding = generate_embedding(
            candidate_text
        )

        record = prepare_embedding_record(

            candidate,

            candidate_text,

            embedding

        )

        insert_candidate_embedding(
            record
        )

        if idx % 1000 == 0:

            print(

                f"{idx}/{total} candidates indexed."

            )

    print(

        "\nBulk indexing completed."

    )