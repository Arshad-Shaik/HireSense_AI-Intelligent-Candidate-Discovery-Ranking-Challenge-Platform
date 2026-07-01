# ai-service/ingestion/job_description_loader.py

from pathlib import Path
from docx import Document


def load_job_description(file_path: str) -> str:
    """
    Load job description from .docx file.

    Returns:
        Entire job description text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description file not found: {file_path}"
        )

    document = Document(file_path)

    paragraphs = [p.text for p in document.paragraphs]

    text = "\n".join(paragraphs)

    return text