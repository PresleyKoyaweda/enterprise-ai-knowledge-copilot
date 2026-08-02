from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="La question posée par l'utilisateur en langage naturel",
        examples=["Quel est le traitement recommandé pour le paludisme grave ?"],
    )


class Source(BaseModel):
    document_name: str
    excerpt: str
    score: float
    rerank_score: int | None = None


class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]
