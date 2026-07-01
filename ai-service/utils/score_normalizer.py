# ai-service/utils/score_normalizer.py

from typing import List, Dict


def normalize_scores(
    ranked_candidates: List[Dict],
) -> List[Dict]:
    """
    Normalize raw scores to [0.0, 1.0] range.

    Steps:
        1. Find min and max score in ranked list.
        2. Normalize each score to [0, 1].
        3. Sort by normalized_score descending.
           Tie-break: candidate_id ascending.
           This satisfies submission_spec.md Section 3.

    Args:
        ranked_candidates: List of candidate dicts with 'score' key.

    Returns:
        List sorted by normalized_score descending,
        candidate_id ascending on tie.
    """

    if not ranked_candidates:
        return []

    scores = [
        item["score"]
        for item in ranked_candidates
    ]

    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score

    for item in ranked_candidates:
        if score_range > 0:
            item["normalized_score"] = round(
                (item["score"] - min_score) / score_range,
                6,
            )
        else:
            # All scores equal → all get 1.0
            item["normalized_score"] = 1.0

    # Sort by normalized_score descending
    # Tie-break: candidate_id ascending
    # This matches submission_spec.md Section 3 exactly
    ranked_candidates.sort(
        key=lambda x: (
            -x["normalized_score"],
            x.get("candidate_id", "")
        )
    )

    return ranked_candidates