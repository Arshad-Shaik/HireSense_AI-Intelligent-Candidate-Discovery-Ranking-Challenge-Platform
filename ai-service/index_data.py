# ai-service/index_data.py

# Phase 2 with better instructions implemented.

from ingestion.candidate_loader import (
    load_candidates
)

from indexing.bulk_indexer import (
    index_candidates
)


def main():

    print("Step 1")

    candidates = load_candidates(
        "../data/candidates.jsonl"
    )

    print("Loaded:", len(candidates))

    print("Step 2")

    index_candidates(
        candidates
    )

    print("Step 3")


if __name__ == "__main__":
    main()












# # ai-service/index_data.py

# Phase 1 Implemented

# from ingestion.candidate_loader import (
#     load_candidates
# )

# from indexing.bulk_indexer import (
#     index_candidates
# )


# def main():

#     candidates = load_candidates(
#         "../data/candidates.jsonl"
#     )

#     index_candidates(
#         candidates
#     )


# if __name__ == "__main__":
#     main()

