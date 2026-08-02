from pathlib import Path

from docx import Document

from app.services.document_extraction import extract_text


def _create_temp_docx(tmp_path: Path, content: str) -> Path:
    file_path = tmp_path / "test_document.docx"
    document = Document()
    document.add_paragraph(content)
    document.save(file_path)
    return file_path


def test_extract_text_from_docx(tmp_path: Path) -> None:
    file_path = _create_temp_docx(tmp_path, "Ceci est un document de test.")

    result = extract_text(file_path)

    assert "Ceci est un document de test." in result


def test_extract_text_raises_on_unsupported_format(tmp_path: Path) -> None:
    unsupported_file = tmp_path / "image.png"
    unsupported_file.write_bytes(b"fake image content")

    try:
        extract_text(unsupported_file)
        assert False, "Une exception ValueError aurait dû être levée"
    except ValueError:
        pass
