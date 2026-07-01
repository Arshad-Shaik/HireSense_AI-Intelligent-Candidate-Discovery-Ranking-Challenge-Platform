# ai-service/pipeline/submission_pipeline.py


def build_submission_row(

        candidate_id,

        rank,

        score,

        explanation

):

    return {

        "candidate_id": candidate_id,

        "rank": rank,

        "score": round(score, 4),

        "reasoning":
        explanation["recommendation"]

    }