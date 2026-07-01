# ai-service/pipeline/semantic_ranking_pipeline.py

import logging
from typing import Dict, List

from retrieval.retriever import (
    retrieve_top_candidates,
)

from filters.candidate_domain_filter import (
    is_relevant_candidate,
)

from features.feature_vector_builder import (
    build_feature_vector,
)

from ranking.ranker import (
    rank_candidate_with_breakdown,
)

from explainability.csv_reasoning_builder import (
    build_csv_reasoning,
)


logger = logging.getLogger(__name__)


def rank_retrieved_candidates(
    candidates_dict: Dict,
    job_description: str,
    top_k: int = 30000,
) -> List[Dict]:
    """
    Full semantic ranking pipeline.

    Step 1: ChromaDB retrieval with BGE query prefix applied.
    Step 2: Domain filter blocks non-IT profiles.
    Step 3: Feature vector per passing candidate.
    Step 4: Final score with breakdown.
    Step 5: CSV reasoning from breakdown.
    Step 6: Sort by score descending once outside loop.
    """

    # Step 1: Retrieve
    search_results = retrieve_top_candidates(
        job_description,
        top_k,
    )

    candidate_ids = search_results["ids"][0]
    distances     = search_results["distances"][0]

    # Step 2: Diagnostics before processing
    if not distances:
        print("\nNo candidates retrieved from ChromaDB.")
        return []

    similarities = [max(0.0, 1.0 - d) for d in distances]

    print("\n----- RETRIEVAL STATS -----")
    print(f"Total retrieved      : {len(candidate_ids)}")
    print(f"Min Distance         : {min(distances):.6f}")
    print(f"Max Distance         : {max(distances):.6f}")
    print(f"Avg Distance         : "
          f"{sum(distances)/len(distances):.6f}")
    print(f"Min Similarity       : {min(similarities):.6f}")
    print(f"Max Similarity       : {max(similarities):.6f}")
    print(f"Avg Similarity       : "
          f"{sum(similarities)/len(similarities):.6f}")

    # Step 3: Process candidates
    ranked_candidates: List[Dict] = []
    filter_pass = 0
    filter_fail = 0
    lookup_miss = 0

    for candidate_id, distance in zip(candidate_ids, distances):

        if candidate_id not in candidates_dict:
            lookup_miss += 1
            continue

        candidate = candidates_dict[candidate_id]

        if not is_relevant_candidate(candidate, job_description):
            filter_fail += 1
            continue

        filter_pass += 1

        feature_vector   = build_feature_vector(candidate)
        similarity_score = max(0.0, 1.0 - distance)

        final_score, breakdown = rank_candidate_with_breakdown(
            feature_vector,
            similarity_score,
        )

        reasoning = build_csv_reasoning(
            candidate=candidate,
            breakdown=breakdown,
            final_score=final_score,
        )

        ranked_candidates.append(
            {
                "candidate_id": candidate_id,
                "score":        final_score,
                "candidate":    candidate,
                "reasoning":    reasoning,
                "breakdown":    breakdown,
            }
        )

    # Step 4: Pipeline diagnostics
    print("\n----- PIPELINE STATS -----")
    print(f"Lookup misses        : {lookup_miss}")
    print(f"Domain filter PASS   : {filter_pass}")
    print(f"Domain filter FAIL   : {filter_fail}")
    print(f"Final candidates     : {len(ranked_candidates)}")

    if len(ranked_candidates) == 0:
        print("\nWARNING: Zero candidates passed the pipeline.")
        print("  1. Verify BGE query prefix in query_embedding.py")
        print("  2. Check domain filter thresholds")
        print("  3. Verify candidate_id consistency")

    # Step 5: Sort ONCE outside loop
    ranked_candidates.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    return ranked_candidates









