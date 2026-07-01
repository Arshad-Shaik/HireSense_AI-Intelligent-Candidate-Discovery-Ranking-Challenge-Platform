# ai-service/ingestion/schema_loader.py

import json
from pathlib import Path


def load_schema(file_path: str) -> dict:
    """
    Load candidate schema JSON.

    Returns:
        Dictionary containing schema.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    return schema