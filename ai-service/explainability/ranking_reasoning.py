# ai-service/explainability/ranking_reasoning.py

def build_ranking_reasoning(
        feature_vector
):

    reasons = []

    if feature_vector[
        "offer_acceptance_rate"
    ] > 0.7:

        reasons.append(
            "High offer acceptance rate"
        )

    if feature_vector[
        "interview_completion_rate"
    ] > 0.7:

        reasons.append(
            "High interview completion rate"
        )

    if feature_vector[
        "github_activity_score"
    ] > 50:

        reasons.append(
            "Strong GitHub activity"
        )

    return reasons