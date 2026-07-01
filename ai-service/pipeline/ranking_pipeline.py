# ai-service/pipeline/ranking_pipeline.py

from features.feature_vector_builder import (
    build_feature_vector
)

from ranking.similarity_score import (
    compute_similarity_score
)

from ranking.ranker import (
    rank_candidate
)


def score_candidate(
        candidate,
        similarity_score
):

    feature_vector = build_feature_vector(
        candidate
    )

    final_score = rank_candidate(

        feature_vector,

        similarity_score

    )

    return final_score