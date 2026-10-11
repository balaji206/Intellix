from dataclasses import dataclass

from app.services.parser import Section


@dataclass
class Chunk:
    text: str
    chunk_index: int
    page: int | None = None


def chunk_sections(
    sections: list[Section],
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[Chunk]:
    """Fixed-size character chunking with overlap, keeping page numbers."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    index = 0

    for section in sections:
        text = section.text
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))

            # try to end on a natural boundary (paragraph, then sentence, then space)
            if end < len(text):
                window = text[start:end]
                cut = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
                if cut > chunk_size * 0.5:
                    end = start + cut + 1

            piece = text[start:end].strip()
            if piece:
                chunks.append(Chunk(text=piece, chunk_index=index, page=section.page))
                index += 1

            if end >= len(text):
                break
            start = max(end - overlap, start + 1)

    return chunks 