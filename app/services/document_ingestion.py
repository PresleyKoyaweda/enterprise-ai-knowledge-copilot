from pathlib import Path

from app.services.document_extraction import extract_text
from app.services.text_chunking import chunk_text

UPLOAD_DIR = Path("data/uploads")


def save_uploaded_file(filename: str, content: bytes) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = UPLOAD_DIR / filename
    file_path.write_bytes(content)
    return file_path


def ingest_document(filename: str, content: bytes) -> tuple[list[str], str]:
    file_path = save_uploaded_file(filename, content)

    text = extract_text(file_path)
    chunks = chunk_text(text)

    return chunks, text