 # ai-service/ranking/ranker.py

import math
import logging
from typing import Dict, Tuple

from ranking.scorer import (
    compute_experience_score,
    compute_skill_score,
    compute_behavior_score,
    compute_trust_score,
    compute_profile_score,
)

from ranking.boost_engine import (
    compute_boost_score,
)

from ranking.penalty_engine import (
    compute_penalty_score,
)

from ranking.weighted_score import (
    compute_weighted_score,
)


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCORE_MIN:       float = 0.0
SCORE_MAX:       float = 1.0
SIMILARITY_MIN:  float = 0.0
SIMILARITY_MAX:  float = 1.0
SCORE_PRECISION: int   = 6


# ---------------------------------------------------------------------------
# Validation Helpers
# ---------------------------------------------------------------------------

def _validate_similarity_score(
    similarity_score: float,
) -> float:
    """
    Validate and clamp similarity score to [0.0, 1.0].
    """
    if not isinstance(similarity_score, (int, float)):
        logger.warning(
            "Invalid similarity_score type: %s. Defaulting to 0.0.",
            type(similarity_score),
        )
        return 0.0

    if math.isnan(similarity_score) or math.isinf(similarity_score):
        logger.warning(
            "similarity_score is NaN or Inf. Defaulting to 0.0."
        )
        return 0.0

    if (
        similarity_score < SIMILARITY_MIN
        or similarity_score > SIMILARITY_MAX
    ):
        logger.warning(
            "similarity_score %.4f out of range. Clamping.",
            similarity_score,
        )
        return max(
            SIMILARITY_MIN,
            min(SIMILARITY_MAX, similarity_score),
        )

    return float(similarity_score)


def _validate_feature_vector(
    feature_vector: dict,
) -> dict:
    """
    Validate feature vector is a dict.
    Returns empty dict on failure for graceful degradation.
    """
    if not isinstance(feature_vector, dict):
        logger.warning(
            "Invalid feature_vector type: %s. Using empty dict.",
            type(feature_vector),
        )
        return {}
    return feature_vector


def _safe_score(
    value,
    name: str,
    default: float = 0.0,
) -> float:
    """
    Safely cast scorer output to float.
    Returns default on failure.
    """
    try:
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            raise ValueError(f"{name} is NaN or Inf")
        return result
    except (TypeError, ValueError) as e:
        logger.warning(
            "Score error for %s: %s. Using %.4f.",
            name, e, default,
        )
        return default


# ---------------------------------------------------------------------------
# Score Breakdown
# ---------------------------------------------------------------------------

def compute_score_breakdown(
    feature_vector: dict,
    similarity_score: float,
) -> Dict[str, float]:
    """
    Compute all individual scoring components.

    Returns named dict with all component scores.
    Used by rank_candidate_with_breakdown() and
    csv_reasoning_builder for rich explainability.

    Returns:
        Dict with keys:
            similarity_score
            experience_score
            skill_score
            behavior_score
            trust_score
            profile_score
            boost_score
            penalty_score
    """

    experience_score = _safe_score(
        compute_experience_score(feature_vector),
        "experience_score",
    )

    skill_score = _safe_score(
        compute_skill_score(feature_vector),
        "skill_score",
    )

    behavior_score = _safe_score(
        compute_behavior_score(feature_vector),
        "behavior_score",
    )

    trust_score = _safe_score(
        compute_trust_score(feature_vector),
        "trust_score",
    )

    profile_score = _safe_score(
        compute_profile_score(feature_vector),
        "profile_score",
    )

    boost_score = _safe_score(
        compute_boost_score(feature_vector),
        "boost_score",
    )

    penalty_score = _safe_score(
        compute_penalty_score(feature_vector),
        "penalty_score",
    )

    return {
        "similarity_score": round(similarity_score, SCORE_PRECISION),
        "experience_score": round(experience_score, SCORE_PRECISION),
        "skill_score":      round(skill_score,      SCORE_PRECISION),
        "behavior_score":   round(behavior_score,   SCORE_PRECISION),
        "trust_score":      round(trust_score,       SCORE_PRECISION),
        "profile_score":    round(profile_score,    SCORE_PRECISION),
        "boost_score":      round(boost_score,       SCORE_PRECISION),
        "penalty_score":    round(penalty_score,    SCORE_PRECISION),
    }


# ---------------------------------------------------------------------------
# Main Ranking Entry Point
# ---------------------------------------------------------------------------

def rank_candidate(
    feature_vector: dict,
    similarity_score: float,
) -> float:
    """
    Production ranking engine.

    Returns single final score as float.
    Use rank_candidate_with_breakdown() when
    you also need the component breakdown
    for explainability.

    Args:
        feature_vector:   From feature_vector_builder.
        similarity_score: Cosine similarity from ChromaDB.

    Returns:
        float: Final score clamped to [0.0, 1.0].
    """

    feature_vector   = _validate_feature_vector(feature_vector)
    similarity_score = _validate_similarity_score(similarity_score)

    breakdown = compute_score_breakdown(
        feature_vector=feature_vector,
        similarity_score=similarity_score,
    )

    try:
        raw_score = compute_weighted_score(
            similarity_score=breakdown["similarity_score"],
            experience_score=breakdown["experience_score"],
            skill_score=breakdown["skill_score"],
            behavior_score=breakdown["behavior_score"],
            trust_score=breakdown["trust_score"],
            profile_score=breakdown["profile_score"],
            boost_score=breakdown["boost_score"],
            penalty_score=breakdown["penalty_score"],
        )
    except Exception as e:
        logger.error(
            "compute_weighted_score failed: %s. "
            "Falling back to similarity_score.",
            e,
        )
        raw_score = similarity_score

    final_score = max(SCORE_MIN, min(SCORE_MAX, raw_score))

    return round(final_score, SCORE_PRECISION)


# ---------------------------------------------------------------------------
# Extended Entry Point — Returns Score + Breakdown
# ---------------------------------------------------------------------------

def rank_candidate_with_breakdown(
    feature_vector: dict,
    similarity_score: float,
) -> Tuple[float, Dict[str, float]]:
    """
    Extended ranking engine.

    Returns final score AND full component breakdown.

    Used by:
        semantic_ranking_pipeline.py
        csv_reasoning_builder.py

    Args:
        feature_vector:   From feature_vector_builder.
        similarity_score: Cosine similarity from ChromaDB.

    Returns:
        Tuple of:
            final_score : float
            breakdown   : Dict[str, float] with all components
                          including final_score key
    """

    feature_vector   = _validate_feature_vector(feature_vector)
    similarity_score = _validate_similarity_score(similarity_score)

    breakdown = compute_score_breakdown(
        feature_vector=feature_vector,
        similarity_score=similarity_score,
    )

    try:
        raw_score = compute_weighted_score(
            similarity_score=breakdown["similarity_score"],
            experience_score=breakdown["experience_score"],
            skill_score=breakdown["skill_score"],
            behavior_score=breakdown["behavior_score"],
            trust_score=breakdown["trust_score"],
            profile_score=breakdown["profile_score"],
            boost_score=breakdown["boost_score"],
            penalty_score=breakdown["penalty_score"],
        )
    except Exception as e:
        logger.error(
            "compute_weighted_score failed: %s. "
            "Falling back to similarity_score.",
            e,
        )
        raw_score = similarity_score

    final_score = max(SCORE_MIN, min(SCORE_MAX, raw_score))
    final_score = round(final_score, SCORE_PRECISION)

    breakdown["final_score"] = final_score

    return final_score, breakdown