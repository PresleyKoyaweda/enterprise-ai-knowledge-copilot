CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

def chunk_text (text :str, chunk_size : int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:

    if overlap >= chunk_size:

        raise ValueError("overlap doit être strictement inférieur à chunk_size")

    chunks : list[str] = []
    start = 0
    text_length = len(text)

    while start < text_length :
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk :
            chunks.append(chunk)


        start += chunk_size - overlap

    return chunks