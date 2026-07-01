# ai-service/explainability/feature_reasoning.py

def build_feature_reasoning(
        feature_vector
):

    reasons = []

    reasons.append(
        f"{feature_vector['years_of_experience']} years of experience"
    )

    reasons.append(
        f"{feature_vector['skill_count']} skills"
    )

    reasons.append(
        f"Profile completeness score {feature_vector['profile_completeness_score']}"
    )

    if feature_vector["verified_email"]:
        reasons.append(
            "Verified email"
        )

    if feature_vector["verified_phone"]:
        reasons.append(
            "Verified phone"
        )

    return reasons