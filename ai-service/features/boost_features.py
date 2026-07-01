# ai-service/features/boost_features.py

def calculate_boost_score(
        candidate
):

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    boost = 0.0

    if signals.get(
            "open_to_work_flag",
            False
    ):
        boost += 0.08

    if signals.get(
            "github_activity_score",
            0
    ) >= 50:
        boost += 0.05

    if signals.get(
            "saved_by_recruiters_30d",
            0
    ) >= 3:
        boost += 0.05

    if signals.get(
            "profile_completeness_score",
            0
    ) >= 80:
        boost += 0.05

    return round(
        boost,
        4
    )