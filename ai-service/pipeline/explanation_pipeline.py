# ai-service/pipeline/explanation_pipeline.py

from features.feature_vector_builder import (
    build_feature_vector
)

from explainability.explanation_pipeline import (
    explain_candidate
)


def generate_candidate_explanation(
        candidate
):

    feature_vector = build_feature_vector(
        candidate
    )

    explanation = explain_candidate(
        feature_vector
    )

    return explanation