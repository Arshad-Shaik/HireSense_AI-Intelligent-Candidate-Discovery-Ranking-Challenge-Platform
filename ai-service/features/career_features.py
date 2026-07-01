# ai-service/features/career_features.py

def extract_career_features(
        candidate
):
    """
    Career progression signals.

    No hardcoded domains.
    """

    career_history = candidate.get(
        "career_history",
        []
    )

    total_roles = len(
        career_history
    )

    companies = set()

    for job in career_history:

        companies.add(

            job.get(
                "company",
                ""
            )

        )

    unique_companies = len(
        companies
    )

    stability_score = 0

    if total_roles > 0:

        stability_score = (

            unique_companies
            /
            total_roles

        )

    return {

        "career_roles_count":
            total_roles,

        "unique_companies_count":
            unique_companies,

        "career_stability_score":
            round(
                stability_score,
                4
            )

    }