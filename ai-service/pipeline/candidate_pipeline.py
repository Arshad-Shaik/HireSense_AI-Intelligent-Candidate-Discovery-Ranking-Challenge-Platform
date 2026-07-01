# ai-service/pipeline/candidate_pipeline.py

from retrieval.retriever import (
    retrieve_top_candidates
)


def get_candidate_pool(
        job_description,
        top_k=1000
):

    results = retrieve_top_candidates(

        job_description,

        top_k

    )

    return results