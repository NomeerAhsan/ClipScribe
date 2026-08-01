import tempfile
from pathlib import Path

from backend.document_writer import DocumentWriter


def test_append_highlight_creates_document():
    with tempfile.TemporaryDirectory() as tmp:
        doc_path = Path(tmp) / "Research.docx"
        state_path = Path(tmp) / ".clipscribe_state.json"
        writer = DocumentWriter(doc_path, state_path)

        status, number = writer.append_highlight(
            html="<p>First <strong>highlight</strong></p>",
            page_title="Example Article",
            page_url="https://example.com/article",
            captured_at="2026-08-01T14:45:00+05:00",
        )

        assert status == "saved"
        assert number == 1
        assert doc_path.exists()


def test_duplicate_highlight_is_detected():
    with tempfile.TemporaryDirectory() as tmp:
        doc_path = Path(tmp) / "Research.docx"
        state_path = Path(tmp) / ".clipscribe_state.json"
        writer = DocumentWriter(doc_path, state_path)

        payload = {
            "html": "<p>Duplicate test</p>",
            "page_title": "Example",
            "page_url": "https://example.com/dup",
            "captured_at": "2026-08-01T14:45:00+05:00",
        }

        writer.append_highlight(**payload)
        status, number = writer.append_highlight(**payload)

        assert status == "duplicate"
        assert number == 0
