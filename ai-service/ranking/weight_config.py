# ai-service/ranking/weight_config.py

"""
Production ranking weights.

Designed using your observed dataset:

Distance Range:
    0.6526 -> 0.8156

Similarity Range:
    0.1843 -> 0.3474

Observations:

1. Semantic retrieval already determines
   relevance.

2. Similarity differences are small.

3. Profile signals should improve ordering
   but never overpower semantic relevance.

4. Recruiter engagement should help but
   should never rank HR Managers above
   AI Engineers.

5. Trust and profile quality should be
   secondary ranking signals.

Final Philosophy:

    Semantic Similarity
        ↓
    Skills
        ↓
    Experience
        ↓
    Profile Quality
        ↓
    Behavior
        ↓
    Trust

"""

WEIGHTS = {

    #
    # Core semantic relevance
    #
    "similarity": 0.70,

    #
    # Candidate capability
    #
    "skills": 0.12,

    #
    # Professional maturity
    #
    "experience": 0.08,

    #
    # Profile quality
    #
    "profile": 0.04,

    #
    # Recruiter engagement
    #
    "behavior": 0.03,

    #
    # Verification / trust
    #
    "trust": 0.03

}


def get_total_weight():

    return round(

        sum(
            WEIGHTS.values()
        ),

        4
    )


def validate_weights():
    """
    Ensures weights sum to 1.0
    during startup.
    """

    total = get_total_weight()

    if abs(total - 1.0) > 0.0001:

        raise ValueError(

            f"Invalid ranking weights. "
            f"Expected 1.0 but got {total}"

        )


validate_weights()