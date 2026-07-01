# ai-service/ranking/weighted_score.py

from ranking.weight_config import (
    WEIGHTS
)


def _clamp(
        value,
        minimum=0.0,
        maximum=1.0
):
    return max(
        minimum,
        min(
            value,
            maximum
        )
    )


def compute_weighted_score(

        similarity_score,

        experience_score,

        skill_score,

        behavior_score,

        trust_score,

        profile_score,

        boost_score,

        penalty_score

):
    """
    Production ranking score.

    Philosophy:

    1. Semantic similarity dominates ranking.

    2. Profile signals help separate
       equally relevant candidates.

    3. Boosts and penalties should
       fine-tune ranking rather than
       overpower semantic relevance.

    4. Final score remains bounded.

    Output:
        0.0 -> 1.0+
    """

    similarity_score = _clamp(
        similarity_score
    )

    experience_score = _clamp(
        experience_score
    )

    skill_score = _clamp(
        skill_score
    )

    behavior_score = _clamp(
        behavior_score
    )

    trust_score = _clamp(
        trust_score
    )

    profile_score = _clamp(
        profile_score
    )

    weighted_core_score = (

        WEIGHTS["similarity"]
        * similarity_score

        +

        WEIGHTS["experience"]
        * experience_score

        +

        WEIGHTS["skills"]
        * skill_score

        +

        WEIGHTS["behavior"]
        * behavior_score

        +

        WEIGHTS["trust"]
        * trust_score

        +

        WEIGHTS["profile"]
        * profile_score

    )

    #
    # Controlled boost contribution
    #
    # Prevent boost inflation.
    #

    boost_adjustment = min(
        boost_score,
        0.08
    )

    #
    # Controlled penalty contribution
    #
    # Prevent excessive punishment.
    #

    penalty_adjustment = min(
        penalty_score,
        0.10
    )

    final_score = (

        weighted_core_score

        +

        boost_adjustment

        -

        penalty_adjustment

    )

    #
    # Protect against negatives.
    #

    final_score = max(
        final_score,
        0.0
    )

    return round(
        final_score,
        6
    )