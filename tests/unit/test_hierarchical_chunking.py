from app.services.hierarchical_chunking import hierarchical_chunk_text


def test_hierarchical_chunk_keeps_short_paragraphs_intact() -> None:
    text = (
        "Ceci est un premier paragraphe suffisamment long pour former une section a part entiere.\n\n"
        "Voici un second paragraphe, lui aussi assez long pour ne pas etre fusionne avec un autre."
    )

    result = hierarchical_chunk_text(text)

    assert len(result) == 2
    assert "premier paragraphe" in result[0]
    assert "second paragraphe" in result[1]


def test_hierarchical_chunk_merges_short_sections() -> None:
    text = "Titre court\n\nUn paragraphe normal qui suit juste apres un titre isole tres bref."

    result = hierarchical_chunk_text(text)

    assert len(result) == 1
    assert "Titre court" in result[0]
    assert "paragraphe normal" in result[0]


def test_hierarchical_chunk_splits_long_section() -> None:
    long_paragraph = "Phrase repetee pour allonger le texte. " * 40

    result = hierarchical_chunk_text(long_paragraph)

    assert len(result) > 1
    assert all(len(chunk) <= 900 for chunk in result)
