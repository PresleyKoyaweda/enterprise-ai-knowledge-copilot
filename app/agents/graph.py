from langgraph.graph import StateGraph, END

from app.agents.state import RAGState
from app.agents.safety_agent import safety_agent
from app.agents.retrieval_agent import retrieval_agent
from app.agents.ranking_agent import ranking_agent
from app.agents.answer_agent import answer_agent
from app.agents.citation_agent import citation_agent


def _route_after_safety(state: RAGState) -> str:
    if state["is_safe"]:
        return "retrieval"
    return END


def _route_after_ranking(state: RAGState) -> str:
    if state["has_relevant_context"]:
        return "answer"
    return END


def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("safety", safety_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("ranking", ranking_agent)
    graph.add_node("answer", answer_agent)
    graph.add_node("citation", citation_agent)

    graph.set_entry_point("safety")

    graph.add_conditional_edges(
        "safety",
        _route_after_safety,
        {"retrieval": "retrieval", END: END},
    )

    graph.add_edge("retrieval", "ranking")

    graph.add_conditional_edges(
        "ranking",
        _route_after_ranking,
        {"answer": "answer", END: END},
    )

    graph.add_edge("answer", "citation")
    graph.add_edge("citation", END)

    return graph.compile()