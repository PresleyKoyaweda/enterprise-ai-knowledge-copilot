from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="La question posée par l'utilisateur en langage naturel",
        examples=["Quelle est la politique de sauvegarde des données ?"],
    )


class Source(BaseModel):
    document_name: str
    excerpt: str
    score: float


class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]