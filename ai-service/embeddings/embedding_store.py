# ai-service/embeddings/embedding_store.py


def prepare_embedding_record(
        candidate,
        candidate_text,
        embedding
):

    record = {

        "candidate_id":

        candidate[
            "candidate_id"
        ],

        "document":

        candidate_text,

        "embedding":

        embedding,

        "metadata": {

            "current_title":

            candidate[
                "profile"
            ].get(
                "current_title",
                ""
            ),

            "location":

            candidate[
                "profile"
            ].get(
                "location",
                ""
            ),

            "years_of_experience":

            candidate[
                "profile"
            ].get(
                "years_of_experience",
                0
            )

        }

    }

    return record