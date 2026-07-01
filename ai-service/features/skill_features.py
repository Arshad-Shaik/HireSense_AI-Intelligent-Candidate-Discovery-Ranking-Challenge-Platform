# ai-service/features/skill_features.py

def extract_skill_features(candidate: dict) -> dict:
    """
    Extract skill-related information.
    """

    skills = candidate.get("skills", [])

    skill_names = [
        skill.get("name", "")
        for skill in skills
    ]

    total_endorsements = sum(
        skill.get("endorsements", 0)
        for skill in skills
    )

    avg_skill_duration = 0

    if skills:
        avg_skill_duration = (
            sum(
                skill.get("duration_months", 0)
                for skill in skills
            ) / len(skills)
        )

    return {

        "skill_count": len(skills),

        "skill_names": skill_names,

        "total_skill_endorsements": total_endorsements,

        "average_skill_duration_months":
            round(avg_skill_duration, 2)
    }