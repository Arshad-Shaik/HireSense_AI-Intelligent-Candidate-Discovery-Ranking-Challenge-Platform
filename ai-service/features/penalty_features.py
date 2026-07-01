# ai-service/features/penalty_features.py

def calculate_penalty_score(
        candidate
):

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    penalty = 0.0

    if signals.get(
            "recruiter_response_rate",
            0
    ) < 0.30:
        penalty += 0.10

    if signals.get(
            "github_activity_score",
            0
    ) < 10:
        penalty += 0.05

    if signals.get(
            "profile_completeness_score",
            100
    ) < 60:
        penalty += 0.05

    if signals.get(
            "notice_period_days",
            0
    ) > 90:
        penalty += 0.05

    return round(
        penalty,
        4
    )