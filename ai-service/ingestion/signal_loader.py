# ai-service/ingestion/signal_loader.py

from pathlib import Path
from docx import Document


def load_signals(file_path: str) -> str:
    """
    Load Redrob signals document.

    Returns:
        Full signal documentation text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Signal document not found: {file_path}"
        )

    document = Document(file_path)

    paragraphs = [p.text for p in document.paragraphs]

    text = "\n".join(paragraphs)

    return text