# ai-service/ranking/scorer.py

def _clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(value, maximum))


def compute_experience_score(feature_vector: dict) -> float:
    """
    Experience score based on years of experience.
    Saturation at 15 years.
    Returns 0.0 to 1.0.
    """
    years = float(
        feature_vector.get("years_of_experience", 0) or 0
    )
    score = years / 15.0
    return round(_clamp(score), 4)


def compute_skill_score(feature_vector: dict) -> float:
    """
    Skill quality score.

    Uses:
        skill_count              → breadth
        total_skill_endorsements → peer validation
        average_skill_duration   → depth
        avg_assessment_score     → platform-verified skill quality
        github_activity_score    → real-world technical evidence

    Returns 0.0 to 1.0.
    """
    skill_count = float(
        feature_vector.get("skill_count", 0) or 0
    )
    endorsements = float(
        feature_vector.get("total_skill_endorsements", 0) or 0
    )
    avg_duration = float(
        feature_vector.get("average_skill_duration_months", 0) or 0
    )
    avg_assessment = float(
        feature_vector.get("avg_assessment_score", 0) or 0
    )
    github_score = float(
        feature_vector.get("github_activity_score", 0) or 0
    )

    skill_count_score  = _clamp(skill_count / 20.0)
    endorsement_score  = _clamp(endorsements / 50.0)
    duration_score     = _clamp(avg_duration / 48.0)
    assessment_score   = _clamp(avg_assessment / 100.0)
    github_norm_score  = _clamp(github_score / 100.0)

    score = (
        skill_count_score  * 0.30
        + endorsement_score  * 0.20
        + duration_score     * 0.15
        + assessment_score   * 0.20
        + github_norm_score  * 0.15
    )

    return round(_clamp(score), 4)


def compute_behavior_score(feature_vector: dict) -> float:
    """
    Candidate behavior quality.

    Uses:
        recruiter_response_rate    → engagement
        offer_acceptance_rate      → commitment
        interview_completion_rate  → reliability
        recency_score              → active status
        response_speed_score       → responsiveness
        open_to_work               → availability signal

    Returns 0.0 to 1.0.
    """
    recruiter_response = float(
        feature_vector.get("recruiter_response_rate", 0) or 0
    )
    offer_acceptance = float(
        feature_vector.get("offer_acceptance_rate", 0.5) or 0.5
    )
    interview_completion = float(
        feature_vector.get("interview_completion_rate", 0) or 0
    )
    recency_score = float(
        feature_vector.get("recency_score", 0) or 0
    )
    response_speed = float(
        feature_vector.get("response_speed_score", 0) or 0
    )
    open_to_work = float(
        1.0 if feature_vector.get("open_to_work", False) else 0.0
    )

    score = (
        recruiter_response   * 0.25
        + offer_acceptance   * 0.15
        + interview_completion * 0.20
        + recency_score      * 0.20
        + response_speed     * 0.10
        + open_to_work       * 0.10
    )

    return round(_clamp(score), 4)


def compute_trust_score(feature_vector: dict) -> float:
    """
    Trust and verification score.

    Uses:
        verified_email       → identity verification
        verified_phone       → identity verification
        linkedin_connected   → professional identity
        github_linked        → technical identity

    Returns 0.0 to 1.0.
    """
    score = 0.0

    if feature_vector.get("verified_email", False):
        score += 0.30

    if feature_vector.get("verified_phone", False):
        score += 0.30

    if feature_vector.get("linkedin_connected", False):
        score += 0.20

    if feature_vector.get("github_linked", False):
        score += 0.20

    return round(_clamp(score), 4)


def compute_profile_score(feature_vector: dict) -> float:
    """
    Profile quality score.

    Uses:
        profile_completeness_score  → completeness
        profile_text_length         → richness
        career_stability_score      → stability
        saved_by_recruiters_30d     → recruiter demand
        search_appearance_30d       → platform visibility
        connection_count            → network strength

    Returns 0.0 to 1.0.
    """
    completeness = float(
        feature_vector.get(
            "profile_completeness_score", 0
        ) or 0
    )
    profile_text_length = float(
        feature_vector.get("profile_text_length", 0) or 0
    )
    career_stability = float(
        feature_vector.get("career_stability_score", 0) or 0
    )
    saved_by_recruiters = float(
        feature_vector.get("saved_by_recruiters_30d", 0) or 0
    )
    search_appearance = float(
        feature_vector.get("search_appearance_30d", 0) or 0
    )
    connection_count = float(
        feature_vector.get("connection_count", 0) or 0
    )

    completeness_score    = _clamp(completeness / 100.0)
    text_score            = _clamp(profile_text_length / 1000.0)
    stability_score       = _clamp(career_stability)
    recruiter_demand      = _clamp(saved_by_recruiters / 20.0)
    visibility_score      = _clamp(search_appearance / 500.0)
    network_score         = _clamp(connection_count / 1000.0)

    score = (
        completeness_score * 0.35
        + text_score       * 0.15
        + stability_score  * 0.15
        + recruiter_demand * 0.15
        + visibility_score * 0.10
        + network_score    * 0.10
    )

    return round(_clamp(score), 4)