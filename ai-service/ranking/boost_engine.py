# ai-service/ranking/boost_engine.py

def compute_boost_score(
        feature_vector
):
    """
    Dynamic positive ranking signals.

    Purpose:
        Reward candidates who demonstrate
        stronger engagement, trust,
        visibility and career quality.

    Boosts are intentionally capped so
    semantic relevance remains dominant.
    """

    boost = 0.0

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

    profile_views_received_30d = feature_vector.get(
        "profile_views_received_30d",
        0
    )

    saved_by_recruiters_30d = feature_vector.get(
        "saved_by_recruiters_30d",
        0
    )

    search_appearance_30d = feature_vector.get(
        "search_appearance_30d",
        0
    )

    profile_completeness_score = feature_vector.get(
        "profile_completeness_score",
        0
    )

    career_stability_score = feature_vector.get(
        "career_stability_score",
        0.0
    )

    years_of_experience = feature_vector.get(
        "years_of_experience",
        0
    )

    skill_count = feature_vector.get(
        "skill_count",
        0
    )

    #
    # Recruiter responsiveness
    #

    if recruiter_response_rate >= 0.90:
        boost += 0.020
    elif recruiter_response_rate >= 0.75:
        boost += 0.015

    #
    # Offer acceptance reliability
    #

    if offer_acceptance_rate >= 0.90:
        boost += 0.020
    elif offer_acceptance_rate >= 0.75:
        boost += 0.015

    #
    # Interview reliability
    #

    if interview_completion_rate >= 0.95:
        boost += 0.020
    elif interview_completion_rate >= 0.85:
        boost += 0.015

    #
    # GitHub activity
    #

    if github_activity_score >= 80:
        boost += 0.015
    elif github_activity_score >= 50:
        boost += 0.010

    #
    # Recruiter demand
    #

    if saved_by_recruiters_30d >= 10:
        boost += 0.015
    elif saved_by_recruiters_30d >= 5:
        boost += 0.010

    #
    # Search visibility
    #

    if search_appearance_30d >= 50:
        boost += 0.010
    elif search_appearance_30d >= 25:
        boost += 0.005

    #
    # Profile traffic
    #

    if profile_views_received_30d >= 100:
        boost += 0.010
    elif profile_views_received_30d >= 50:
        boost += 0.005

    #
    # Strong profile quality
    #

    if profile_completeness_score >= 90:
        boost += 0.015
    elif profile_completeness_score >= 80:
        boost += 0.010

    #
    # Career stability
    #

    if career_stability_score >= 0.80:
        boost += 0.010

    #
    # Experience maturity
    #

    if years_of_experience >= 10:
        boost += 0.010

    #
    # Rich skill profile
    #

    if skill_count >= 20:
        boost += 0.010
    elif skill_count >= 15:
        boost += 0.005

    #
    # Safety cap
    #

    boost = min(
        boost,
        0.08
    )

    return round(
        boost,
        6
    )