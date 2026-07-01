# ai-service/output/csv_writer.py

import csv


def write_submission_csv(
        rows,
        output_path="../outputs/HireSense_AI.csv"
):

    with open(

            output_path,

            "w",

            newline="",

            encoding="utf-8"

    ) as file:

        writer = csv.DictWriter(

            file,

            fieldnames=[

                "candidate_id",

                "rank",

                "score",

                "reasoning"

            ]

        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    print(
        "Submission file saved."
    )