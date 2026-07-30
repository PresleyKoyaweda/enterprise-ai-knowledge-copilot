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
        "needs_rag": True,
        "direct_answer": "",
        "context_chunks": [],
        "sources_metadata": [],
        "has_relevant_context": True,
        "answer": "",
    })

    if not result["needs_rag"]:
        return QuestionResponse(
            answer=result["direct_answer"],
            sources=[],
        )

    if not result["is_safe"]:
        return QuestionResponse(
            answer=f"Question refusée : {result['rejection_reason']}",
            sources=[],
        )

    if not result["has_relevant_context"]:
        return QuestionResponse(
            answer="Aucune information pertinente n'a été trouvée dans les documents disponibles pour répondre à cette question.",
            sources=[],
        )

    return QuestionResponse(
        answer=result["answer"],
        sources=[Source(**source) for source in result["sources_metadata"]],
    )