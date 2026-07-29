from app.services.text_chunking import chunk_text


def test_chunk_text_shorter_than_chunk_size_returns_one_chunk() -> None:
    text = "Un texte court."

    result = chunk_text(text, chunk_size=800, overlap=100)

    assert len(result) == 1
    assert result[0] == "Un texte court."


def test_chunk_text_creates_overlap_between_chunks() -> None:
    text = "ABCDEFGHIJKLMNOP"

    result = chunk_text(text, chunk_size=10, overlap=3)

    assert result[0] == "ABCDEFGHIJ"
    assert result[1] == "HIJKLMNOP"


def test_chunk_text_raises_when_overlap_too_large() -> None:
    try:
        chunk_text("un texte quelconque", chunk_size=10, overlap=10)
        assert False, "Une exception ValueError aurait dû être levée"
    except ValueError:
        pass