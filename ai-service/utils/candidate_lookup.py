# ai-service/utils/candidate_lookup.py


def build_candidate_lookup(
        candidates
):

    lookup = {}

    for candidate in candidates:

        lookup[
            candidate[
                "candidate_id"
            ]
        ] = candidate

    return lookup