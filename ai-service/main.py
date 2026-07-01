# ai-service/main.py

from ingestion.candidate_loader import load_candidates
from ingestion.schema_loader import load_schema
from ingestion.job_description_loader import load_job_description
from ingestion.signal_loader import load_signals

from features.feature_vector_builder import (
    build_feature_vector
)

from embeddings.candidate_embedding import (
    build_candidate_text
)

from embeddings.embedding_builder import (
    generate_embedding
)

from embeddings.embedding_store import (
    prepare_embedding_record
)

from retrieval.query_embedding import (
    build_query_embedding
)

from retrieval.topk_retriever import (
    extract_top_candidates
)

from ranking.similarity_score import (
    compute_similarity_score
)

from ranking.ranker import (
    rank_candidate
)

from explainability.explanation_pipeline import (
    explain_candidate
)


def main():

    candidates = load_candidates(
        "../data/candidates.jsonl"
    )

    load_schema(
        "../data/candidate_schema.json"
    )

    job_description = load_job_description(
        "../data/job_description.docx"
    )

    load_signals(
        "../data/redrob_signals_doc.docx"
    )

    print("Candidates loaded:", len(candidates))
    print("Schema loaded.")
    print("Job description loaded.")
    print("Signals loaded.")

    candidate = candidates[0]

    print("\nCandidate ID:")
    print(candidate["candidate_id"])

    feature_vector = build_feature_vector(
        candidate
    )

    print("\nFeature Vector:")
    print(feature_vector)

    candidate_text = build_candidate_text(
        candidate
    )

    embedding = generate_embedding(
        candidate_text
    )

    print(
        "\nEmbedding dimension:",
        len(embedding)
    )

    record = prepare_embedding_record(
        candidate,
        candidate_text,
        embedding
    )

    print(
        "\nEmbedding Record Prepared:",
        record["candidate_id"]
    )

    query_embedding = build_query_embedding(
        job_description
    )

    results = extract_top_candidates(

        query_embedding,

        top_k=5

    )

    print(
        "\nTop Retrieved Candidate IDs:"
    )

    print(
        results["ids"][0]
    )

    similarity_score = compute_similarity_score(
        0.15
    )

    final_score = rank_candidate(

        feature_vector,

        similarity_score

    )

    print(
        "\nFinal Score:",
        final_score
    )

    explanation = explain_candidate(
        feature_vector
    )

    print(
        "\nExplanation:"
    )

    print(
        explanation
    )


if __name__ == "__main__":
    main()