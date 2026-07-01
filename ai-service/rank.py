# ai-service/rank.py

# It is mandatory to run first ai-serviceindex_data.py file for indexing the all data of 100K candidates in chromadb database before running this file. then after this run this file ai-service/rank.py for ranking the candidates to retrieve the top 100 candidates for the given job description and generate the HireSense_AI.csv file in the outputs folder.
"""
rank.py

Main entry point for HireSense_AI ranking pipeline.
Redrob AI Intelligent Candidate Discovery & Ranking Challenge.

Pipeline:
    Load candidates
    → Load JD
    → Build lookup
    → Semantic retrieval + domain filter + ranking
    → Normalize scores
    → Write Top 100 CSV
"""

import sys
import logging

from ingestion.candidate_loader import (
    load_candidates,
)

from ingestion.job_description_loader import (
    load_job_description,
)

from utils.candidate_lookup import (
    build_candidate_lookup,
)

from pipeline.semantic_ranking_pipeline import (
    rank_retrieved_candidates,
)

from utils.score_normalizer import (
    normalize_scores,
)

from output.csv_writer import (
    write_submission_csv,
)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CANDIDATES_PATH: str = "../data/candidates.jsonl"
JD_PATH:         str = "../data/job_description.docx"
TOP_K_RETRIEVE:  int = 30000
TOP_N_FINAL:     int = 100


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """
    End-to-end HireSense_AI ranking pipeline.

    Step 1: Load 100K candidates into memory.
    Step 2: Load job description text.
    Step 3: Build O(1) candidate lookup by candidate_id.
    Step 4: Semantic retrieval + domain filter + ranking.
    Step 5: Sort by score descending.
    Step 6: Normalize scores to [0, 1].
    Step 7: Take Top 100.
    Step 8: Build submission rows.
    Step 9: Write HireSense_AI.csv.
    """

    # Step 1
    print("Step 1: Loading candidates...")
    candidates = load_candidates(CANDIDATES_PATH)
    print(f"        Loaded {len(candidates)} candidates.")

    # Step 2
    print("Step 2: Loading job description...")
    job_description = load_job_description(JD_PATH)

    if not job_description or not job_description.strip():
        print("ERROR: Job description is empty. Cannot rank.")
        sys.exit(1)

    print(f"        JD length: {len(job_description)} characters.")

    # Step 3
    print("Step 3: Building candidate lookup...")
    candidates_dict = build_candidate_lookup(candidates)
    print(f"        Lookup ready: {len(candidates_dict)} entries.")

    # Step 4
    print(f"Step 4: Running semantic ranking pipeline "
          f"(top_k={TOP_K_RETRIEVE})...")

    ranked_candidates = rank_retrieved_candidates(
        candidates_dict=candidates_dict,
        job_description=job_description,
        top_k=TOP_K_RETRIEVE,
    )

    if not ranked_candidates:
        print("\nERROR: Zero candidates ranked.")
        print("Possible causes:")
        print("  1. BGE query prefix missing in query_embedding.py")
        print("  2. Domain filter thresholds too aggressive")
        print("  3. ChromaDB returned 0 results")
        print("  4. candidate_id mismatch between ChromaDB and JSONL")
        sys.exit(1)

    print(f"\n        Ranked candidates: {len(ranked_candidates)}")

    # Step 5
    ranked_candidates.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    # Step 6
    print("Step 5: Normalizing scores...")
    ranked_candidates = normalize_scores(ranked_candidates)

    # Step 7
    top_100 = ranked_candidates[:TOP_N_FINAL]
    print(f"Step 6: Selected Top {len(top_100)} candidates.")

    if len(top_100) < TOP_N_FINAL:
        print(f"WARNING: Only {len(top_100)} candidates available.")
        print("         Lower filter thresholds if needed.")

    # Step 8
    submission_rows = []
    for rank, item in enumerate(top_100, start=1):
        candidate    = item["candidate"]
        candidate_id = item.get(
            "candidate_id",
            candidate.get("candidate_id", f"unknown_{rank}"),
        )
        submission_rows.append(
            {
                "candidate_id": candidate_id,
                "rank":         rank,
                "score":        round(
                    item.get(
                        "normalized_score",
                        item["score"]
                    ),
                    6,
                ),
                "reasoning":    item.get("reasoning", ""),
            }
        )

    # Step 9
    print("Step 7: Writing submission CSV...")
    write_submission_csv(submission_rows)

    # Summary
    print("\n" + "=" * 50)
    print("HireSense_AI ranking complete.")
    print(
        f"Top {len(submission_rows)} candidates "
        f"written to HireSense_AI.csv"
    )
    if submission_rows:
        print(
            f"Score range: "
            f"{submission_rows[-1]['score']:.6f}"
            f" → "
            f"{submission_rows[0]['score']:.6f}"
        )
    print("=" * 50)


if __name__ == "__main__":
    main()














