# ai-service/explainability/explanation_builder.py

from explainability.reason_generator import (
    generate_reason
)


def build_explanation(
        candidate
):
    """
    Build explanation object.
    """

    return {

        "candidate_id":

        candidate[
            "candidate_id"
        ],

        "reasoning":

        generate_reason(
            candidate
        )

    }