# ai-service/features/profile_features.py

def extract_profile_features(
        candidate
):

    profile = candidate.get(
        "profile",
        {}
    )

    headline = profile.get(
        "headline",
        ""
    )

    summary = profile.get(
        "summary",
        ""
    )

    text_length = len(
        headline
    ) + len(
        summary
    )

    return {

        "profile_text_length":
            text_length

    }