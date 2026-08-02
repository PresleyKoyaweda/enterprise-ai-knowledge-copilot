from pathlib import Path

from docx import Document
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def _extract_from_pdf(file_path: Path) -> str:
    reader = PdfReader(file_path)
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text)


def _extract_from_docx(file_path: Path) -> str:
    document = Document(file_path)
    paragraphs_text = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs_text)


def extract_text(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Format de fichier non supporté : {extension}")

    if extension == ".pdf":
        return _extract_from_pdf(file_path)

    return _extract_from_docx(file_path)
