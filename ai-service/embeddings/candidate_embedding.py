# ai-service/embeddings/candidate_embedding.py

def build_candidate_text(
        candidate: dict
) -> str:

    profile = candidate.get(
        "profile",
        {}
    )

    current_title = profile.get(
        "current_title",
        ""
    )

    headline = profile.get(
        "headline",
        ""
    )

    summary = profile.get(
        "summary",
        ""
    )

    years_of_experience = profile.get(
        "years_of_experience",
        0
    )

    current_company = profile.get(
        "current_company",
        ""
    )

    skills = candidate.get(
        "skills",
        []
    )

    skill_names = []

    for skill in skills:

        skill_name = skill.get(
            "name",
            ""
        )

        if skill_name:

            skill_names.append(
                skill_name
            )

    skills_text = " ".join(
        skill_names
    )

    career_history = candidate.get(
        "career_history",
        []
    )

    career_entries = []

    for job in career_history:

        title = job.get(
            "title",
            ""
        )

        company = job.get(
            "company",
            ""
        )

        career_entries.append(

            f"{title}"

        )

        career_entries.append(

            f"{title} at {company}"

        )

    career_text = " ".join(
        career_entries
    )

    document = f"""
PRIMARY_ROLE:
{current_title}

PRIMARY_ROLE_REPEAT:
{current_title}

PRIMARY_ROLE_REPEAT:
{current_title}

HEADLINE:
{headline}

HEADLINE_REPEAT:
{headline}

CORE_SKILLS:
{skills_text}

CORE_SKILLS_REPEAT:
{skills_text}

CAREER_HISTORY:
{career_text}

EXPERIENCE_YEARS:
{years_of_experience}

CURRENT_COMPANY:
{current_company}

SUMMARY:
{summary}
"""

    return document.strip()



























