# ai-service/features/behavior_features.py

from datetime import datetime, date


def _parse_date(date_str) -> datetime:
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str), "%Y-%m-%d")
    except Exception:
        return None


def _days_since(date_str) -> int:
    parsed = _parse_date(date_str)
    if not parsed:
        return 9999
    return (datetime.now() - parsed).days


def extract_behavior_features(candidate: dict) -> dict:
    """
    Extract behavioral engagement signals.

    Uses from redrob_signals schema:
        recruiter_response_rate
        offer_acceptance_rate
        interview_completion_rate
        open_to_work_flag
        last_active_date
        avg_response_time_hours
        applications_submitted_30d
        profile_views_received_30d
        saved_by_recruiters_30d
        search_appearance_30d
        willing_to_relocate
        notice_period_days
        connection_count
        skill_assessment_scores
        github_activity_score
    """
    signals = candidate.get("redrob_signals", {}) or {}

    recruiter_response_rate = float(
        signals.get("recruiter_response_rate", 0) or 0
    )
    offer_acceptance_rate = float(
        signals.get("offer_acceptance_rate", -1) or -1
    )
    # -1 means no prior offers, treat as neutral 0.5
    if offer_acceptance_rate < 0:
        offer_acceptance_rate = 0.5

    interview_completion_rate = float(
        signals.get("interview_completion_rate", 0) or 0
    )

    open_to_work = bool(
        signals.get("open_to_work_flag", False)
    )

    days_since_active = _days_since(
        signals.get("last_active_date", None)
    )
    # Recency score: active within 30 days = 1.0, 90 days = 0.5
    if days_since_active <= 30:
        recency_score = 1.0
    elif days_since_active <= 60:
        recency_score = 0.75
    elif days_since_active <= 90:
        recency_score = 0.5
    elif days_since_active <= 180:
        recency_score = 0.25
    else:
        recency_score = 0.0

    avg_response_hours = float(
        signals.get("avg_response_time_hours", 999) or 999
    )
    # Faster response = higher score
    if avg_response_hours <= 4:
        response_speed_score = 1.0
    elif avg_response_hours <= 24:
        response_speed_score = 0.75
    elif avg_response_hours <= 72:
        response_speed_score = 0.5
    else:
        response_speed_score = 0.25

    applications_30d = int(
        signals.get("applications_submitted_30d", 0) or 0
    )
    profile_views_30d = int(
        signals.get("profile_views_received_30d", 0) or 0
    )
    saved_by_recruiters_30d = int(
        signals.get("saved_by_recruiters_30d", 0) or 0
    )
    search_appearance_30d = int(
        signals.get("search_appearance_30d", 0) or 0
    )
    willing_to_relocate = bool(
        signals.get("willing_to_relocate", False)
    )
    notice_period_days = int(
        signals.get("notice_period_days", 90) or 90
    )
    connection_count = int(
        signals.get("connection_count", 0) or 0
    )

    # Skill assessment scores (AI/ML relevant)
    assessment_scores = signals.get(
        "skill_assessment_scores", {}
    ) or {}
    ai_ml_assessments = []
    for skill_name, score in assessment_scores.items():
        if isinstance(score, (int, float)) and score >= 0:
            ai_ml_assessments.append(float(score))

    avg_assessment_score = (
        sum(ai_ml_assessments) / len(ai_ml_assessments)
        if ai_ml_assessments else 0.0
    )

    # GitHub activity
    github_activity_score = float(
        signals.get("github_activity_score", -1) or -1
    )
    github_score = max(0.0, github_activity_score)

    return {
        "recruiter_response_rate":      recruiter_response_rate,
        "offer_acceptance_rate":        offer_acceptance_rate,
        "interview_completion_rate":    interview_completion_rate,
        "open_to_work":                 open_to_work,
        "recency_score":                recency_score,
        "days_since_active":            days_since_active,
        "response_speed_score":         response_speed_score,
        "avg_response_time_hours":      avg_response_hours,
        "applications_submitted_30d":   applications_30d,
        "profile_views_received_30d":   profile_views_30d,
        "saved_by_recruiters_30d":      saved_by_recruiters_30d,
        "search_appearance_30d":        search_appearance_30d,
        "willing_to_relocate":          willing_to_relocate,
        "notice_period_days":           notice_period_days,
        "connection_count":             connection_count,
        "avg_assessment_score":         avg_assessment_score,
        "github_activity_score":        github_score,
    }