# ai-service/ranking/penalty_engine.py

def compute_penalty_score(
        feature_vector
):
    """
    Dynamic negative ranking signals.

    Purpose:
        Reduce ranking score for candidates
        showing weak engagement, low trust,
        incomplete profiles, or poor quality
        signals.

    Penalties are capped so they do not
    overpower semantic relevance.
    """

    penalty = 0.0

    recruiter_response_rate = feature_vector.get(
        "recruiter_response_rate",
        0.0
    )

    offer_acceptance_rate = feature_vector.get(
        "offer_acceptance_rate",
        0.0
    )

    interview_completion_rate = feature_vector.get(
        "interview_completion_rate",
        0.0
    )

    github_activity_score = feature_vector.get(
        "github_activity_score",
        0
    )

    profile_completeness_score = feature_vector.get(
        "profile_completeness_score",
        0
    )

    verified_email = feature_vector.get(
        "verified_email",
        False
    )

    verified_phone = feature_vector.get(
        "verified_phone",
        False
    )

    linkedin_connected = feature_vector.get(
        "linkedin_connected",
        False
    )

    notice_period_days = feature_vector.get(
        "notice_period_days",
        0
    )

    skill_count = feature_vector.get(
        "skill_count",
        0
    )

    years_of_experience = feature_vector.get(
        "years_of_experience",
        0
    )

    career_roles_count = feature_vector.get(
        "career_roles_count",
        0
    )

    career_stability_score = feature_vector.get(
        "career_stability_score",
        0.0
    )

    #
    # Recruiter responsiveness
    #

    if recruiter_response_rate < 0.20:
        penalty += 0.020

    elif recruiter_response_rate < 0.40:
        penalty += 0.010

    #
    # Offer acceptance
    #

    if offer_acceptance_rate < 0.20:
        penalty += 0.015

    elif offer_acceptance_rate < 0.40:
        penalty += 0.008

    #
    # Interview completion
    #

    if interview_completion_rate < 0.40:
        penalty += 0.020

    elif interview_completion_rate < 0.60:
        penalty += 0.010

    #
    # Very weak GitHub activity
    #

    if github_activity_score < 5:
        penalty += 0.010

    #
    # Profile quality
    #

    if profile_completeness_score < 40:
        penalty += 0.030

    elif profile_completeness_score < 60:
        penalty += 0.015

    #
    # Missing verification signals
    #

    if not verified_email:
        penalty += 0.015

    if not verified_phone:
        penalty += 0.015

    if not linkedin_connected:
        penalty += 0.005

    #
    # Long notice period
    #

    if notice_period_days > 120:
        penalty += 0.020

    elif notice_period_days > 90:
        penalty += 0.010

    #
    # Thin skill profile
    #

    if skill_count < 5:
        penalty += 0.020

    elif skill_count < 10:
        penalty += 0.010

    #
    # Extremely low experience
    #

    if years_of_experience < 1:
        penalty += 0.020

    elif years_of_experience < 2:
        penalty += 0.010

    #
    # Career instability
    #

    if career_roles_count >= 5:

        if career_stability_score < 0.40:
            penalty += 0.015

        elif career_stability_score < 0.60:
            penalty += 0.008

    #
    # Safety cap
    #

    penalty = min(
        penalty,
        0.10
    )

    return round(
        penalty,
        6
    )