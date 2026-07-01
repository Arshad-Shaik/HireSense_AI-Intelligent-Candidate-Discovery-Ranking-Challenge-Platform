# ai-service/ranking/ranking_pipeline.py

from ranking.ranker import (
    rank_candidate
)


def rank_candidates(

        candidate_feature_vectors,

        similarity_scores

):

    ranked_candidates = []

    for feature_vector, similarity_score in zip(

            candidate_feature_vectors,

            similarity_scores

    ):

        score = rank_candidate(

            feature_vector,

            similarity_score

        )

        ranked_candidates.append(

            {

                "candidate_id":

                feature_vector[
                    "candidate_id"
                ],

                "score": score

            }

        )

    ranked_candidates.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return ranked_candidates