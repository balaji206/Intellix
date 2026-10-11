from dataclasses import dataclass
from pathlib import Path

from docx import Document
from pypdf import PdfReader

SUPPORTED = {".pdf", ".docx", ".txt", ".md"}


@dataclass
class Section:
    """A piece of extracted text plus where it came from (for citations)."""
    text: str
    page: int | None = None


def parse_file(path: str | Path) -> list[Section]:
    path = Path(path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED:
        raise ValueError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        return _parse_pdf(path)
    if ext == ".docx":
        return _parse_docx(path)
    return _parse_text(path)


def _parse_pdf(path: Path) -> list[Section]:
    reader = PdfReader(str(path))
    sections = []
    for i, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            sections.append(Section(text=text, page=i))
    return sections


def _parse_docx(path: Path) -> list[Section]:
    doc = Document(str(path))
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return [Section(text=text)] if text else []


def _parse_text(path: Path) -> list[Section]:
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    return [Section(text=text)] if text else []