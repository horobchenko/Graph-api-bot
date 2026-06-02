from pathlib import Path

from services.rag_storage import RAGStorage


def test_read_text_supports_txt(tmp_path: Path) -> None:
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Real estate document for testing purposes.", encoding="utf-8")

    text = RAGStorage._read_text(file_path)

    assert "Real estate document" in text


def test_read_text_supports_docx(tmp_path: Path) -> None:
    try:
        from docx import Document
    except ImportError:
        return

    file_path = tmp_path / "sample.docx"
    doc = Document()
    doc.add_paragraph("Contract clause example")
    doc.save(file_path)

    text = RAGStorage._read_text(file_path)

    assert "Contract clause example" in text
