# ai-service/explainability/explanation_pipeline.py

from explainability.explanation_builder import (
    build_explanation
)


def explain_candidate(
        feature_vector
):

    return build_explanation(
        feature_vector
    )