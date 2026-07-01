# ai-service/explainability/reason_generator.py


def generate_reason(
        candidate
):
    """
    Generate human-readable explanation
    from actual candidate profile and signals.
    """

    profile = candidate.get(
        "profile",
        {}
    )

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    current_title = profile.get(
        "current_title",
        "Professional"
    )

    years = profile.get(
        "years_of_experience",
        0
    )

    skills = len(
        candidate.get(
            "skills",
            []
        )
    )

    profile_score = signals.get(
        "profile_completeness_score",
        0
    )

    recruiter_response_rate = signals.get(
        "recruiter_response_rate",
        0
    )

    verified_email = signals.get(
        "verified_email",
        False
    )

    verified_phone = signals.get(
        "verified_phone",
        False
    )

    explanation = (

    f"{current_title} with "

    f"{years:.1f} years of experience "

    f"and {skills} skills. "

)
    
    github_score = signals.get(
    "github_activity_score",
    0
)

    if github_score >= 50:

        explanation += (
            " Strong engineering activity."
        )

    if profile_score >= 80:

        explanation += (
            " Strong profile quality."
        )

    elif profile_score >= 60:

        explanation += (
            " Good profile completeness."
        )

    else:

        explanation += (
            " Moderate profile completeness."
        )

    if recruiter_response_rate >= 0.70:

        explanation += (
            " High recruiter engagement."
        )

    if verified_email and verified_phone:

        explanation += (
            " Verified contact information."
        )

    return explanation