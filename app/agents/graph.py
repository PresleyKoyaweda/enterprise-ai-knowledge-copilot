from langgraph.graph import END, StateGraph

from app.agents.answer_agent import answer_agent
from app.agents.citation_agent import citation_agent
from app.agents.planner_agent import planner_agent
from app.agents.ranking_agent import ranking_agent
from app.agents.rerank_agent import rerank_agent
from app.agents.retrieval_agent import retrieval_agent
from app.agents.safety_agent import safety_agent
from app.agents.state import RAGState


def _route_after_safety(state: RAGState) -> str:
    if state["is_safe"]:
        return "planner"
    return END


def _route_after_planner(state: RAGState) -> str:
    if state["needs_rag"]:
        return "retrieval"
    return END


def _route_after_ranking(state: RAGState) -> str:
    if state["has_relevant_context"]:
        return "answer"
    return END


def build_rag_graph():
    graph = StateGraph(RAGState)

    graph.add_node("safety", safety_agent)
    graph.add_node("planner", planner_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("ranking", ranking_agent)
    graph.add_node("rerank", rerank_agent)
    graph.add_node("answer", answer_agent)
    graph.add_node("citation", citation_agent)

    graph.set_entry_point("safety")

    graph.add_conditional_edges(
        "safety",
        _route_after_safety,
        {"planner": "planner", END: END},
    )

    graph.add_conditional_edges(
        "planner",
        _route_after_planner,
        {"retrieval": "retrieval", END: END},
    )

    graph.add_edge("retrieval", "ranking")

    graph.add_conditional_edges(
        "ranking",
        _route_after_ranking,
        {"answer": "rerank", END: END},
    )

    graph.add_edge("rerank", "answer")
    graph.add_edge("answer", "citation")
    graph.add_edge("citation", END)

    return graph.compile()