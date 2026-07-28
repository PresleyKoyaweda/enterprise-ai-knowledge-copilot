from fastapi import APIRouter

from app.models.chat import QuestionRequest, QuestionResponse, Source

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    return QuestionResponse(
        answer=f"Réponse simulée à la question : {request.question}",
        sources=[
            Source(
                document_name="politique_securite.pdf",
                excerpt="Extrait factice du document...",
                score=0.87,
            )
        ],
    )