# ai-service/ranking/behavior_ranker.py

def compute_behavior_rank(
        feature_vector
):
    """
    Candidate availability score.
    """

    score = 0.0

    score += (

        feature_vector.get(
            "recruiter_response_rate",
            0
        )

        * 0.35

    )

    score += (

        feature_vector.get(
            "offer_acceptance_rate",
            0
        )

        * 0.30

    )

    score += (

        feature_vector.get(
            "interview_completion_rate",
            0
        )

        * 0.35

    )

    return round(
        score,
        4
    )