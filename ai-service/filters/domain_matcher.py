# ai-service/filters/domain_matcher.py

def compute_domain_match_score(
        candidate
):
    """
    Estimate whether the candidate belongs
    to software / AI / ranking / retrieval domain.
    """

    profile = candidate.get(
        "profile",
        {}
    )

    title = profile.get(
        "current_title",
        ""
    ).lower()

    headline = profile.get(
        "headline",
        ""
    ).lower()

    summary = profile.get(
        "summary",
        ""
    ).lower()

    text = " ".join(

        [

            title,

            headline,

            summary

        ]

    )

    indicators = [

        "engineer",
        "developer",
        "software",
        "backend",
        "frontend",
        "machine learning",
        "ai",
        "search",
        "retrieval",
        "ranking",
        "recommendation",
        "nlp",
        "data"
    ]

    score = 0

    for keyword in indicators:

        if keyword in text:

            score += 1

    return score