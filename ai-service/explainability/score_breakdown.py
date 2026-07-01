# ai-service/explainability/score_breakdown.py

def build_score_breakdown(

        similarity_score,
        experience_score,
        skill_score,
        behavior_score,
        trust_score,
        profile_score,
        boost_score,
        penalty_score

):

    return {

        "similarity_score": similarity_score,

        "experience_score": experience_score,

        "skill_score": skill_score,

        "behavior_score": behavior_score,

        "trust_score": trust_score,

        "profile_score": profile_score,

        "boost_score": boost_score,

        "penalty_score": penalty_score

    }