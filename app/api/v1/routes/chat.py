from fastapi import APIRouter

from app.models.chat import QuestionRequest, QuestionResponse, Source
from app.services.rag import answer_question

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    answer, sources = answer_question(request.question)

    return QuestionResponse(
        answer=answer,
        sources=[Source(**source) for source in sources],
    )