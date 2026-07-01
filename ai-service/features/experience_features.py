# ai-service/features/experience_features.py

def extract_experience_features(
        candidate
):

    profile = candidate.get(
        "profile",
        {}
    )

    career_history = candidate.get(
        "career_history",
        []
    )

    return {

        "years_of_experience":
            profile.get(
                "years_of_experience",
                0
            ),

        "career_transitions":
            len(
                career_history
            )

    }