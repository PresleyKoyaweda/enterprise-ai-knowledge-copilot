from app.services.text_chunking import chunk_text

MAX_SECTION_SIZE = 800
MIN_SECTION_SIZE = 50


def _split_into_sections(text: str) -> list[str]:
    raw_sections = text.split("\n\n")
    sections = [s.strip() for s in raw_sections if s.strip()]

    merged_sections: list[str] = []
    buffer = ""

    for section in sections:
        buffer = f"{buffer}\n\n{section}".strip() if buffer else section

        if len(buffer) >= MIN_SECTION_SIZE:
            merged_sections.append(buffer)
            buffer = ""

    if buffer:
        merged_sections.append(buffer)

    return merged_sections


def hierarchical_chunk_text(text: str) -> list[str]:
    sections = _split_into_sections(text)

    final_chunks: list[str] = []

    for section in sections:
        if len(section) <= MAX_SECTION_SIZE:
            final_chunks.append(section)
        else:
            final_chunks.extend(chunk_text(section))

    return final_chunks