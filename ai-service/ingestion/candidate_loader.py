# ai-service/ingestion/candidate_loader.py

import json
from pathlib import Path


def load_candidates(file_path: str) -> list[dict]:
    """
    Load candidates from a .jsonl file.

    Returns:
        List of candidate dictionaries.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Candidates file not found: {file_path}")

    candidates = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line:
                candidate = json.loads(line)
                candidates.append(candidate)

    return candidates