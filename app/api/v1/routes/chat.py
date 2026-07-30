from fastapi import APIRouter

from app.models.chat import QuestionRequest, QuestionResponse, Source
from app.agents.graph import build_rag_graph

router = APIRouter()

rag_graph = build_rag_graph()


@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest) -> QuestionResponse:
    result = rag_graph.invoke({
        "question": request.question,
        "is_safe": True,
        "rejection_reason": "",
        "context_chunks": [],
        "sources_metadata": [],
        "answer": "",
    })

    if not result["is_safe"]:
        return QuestionResponse(
            answer=f"Question refusée : {result['rejection_reason']}",
            sources=[],
        )

    return QuestionResponse(
        answer=result["answer"],
        sources=[Source(**source) for source in result["sources_metadata"]],
    )