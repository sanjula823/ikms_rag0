import os
from functools import lru_cache

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from app.core.agents.prompts import ANSWER_PROMPT, VERIFICATION_PROMPT
from app.core.agents.state import QAState
from app.core.retrieval.retriever import retrieve_chunks
from app.core.retrieval.serialization import serialize_chunks_with_ids
from app.utils.logging import get_logger
from app.utils.text import extract_citation_ids, remove_invalid_citations


logger = get_logger(__name__)


def get_demo_mode() -> bool:
    """Check if demo mode is enabled"""
    return os.getenv("DEMO_MODE", "false").lower() == "true"


def _retrieve_node(state: QAState) -> QAState:
    docs = retrieve_chunks(state["question"], state.get("top_k", 4))
    context, citation_map = serialize_chunks_with_ids(docs)
    return {"context": context, "citations": citation_map}


def _answer_node(state: QAState) -> QAState:
    if get_demo_mode():
        logger.info("[DEMO MODE] Using mock answer generation")
        answer = "Based on the provided context, this is a demo response [C1]. The system demonstrates how citations work in the context of question answering [C2]. This allows testing the full pipeline without external API keys [C3]."
        logger.info("Citations used in answer: %s", ", ".join(extract_citation_ids(answer)))
        return {"answer": answer}
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    messages = ANSWER_PROMPT.format_messages(
        question=state["question"],
        context=state.get("context", ""),
    )
    response = llm.invoke(messages)
    answer = response.content or ""
    logger.info("Citations used in answer: %s", ", ".join(extract_citation_ids(answer)))
    return {"answer": answer}


def _verify_node(state: QAState) -> QAState:
    citations = state.get("citations") or {}
    valid_ids = sorted(citations.keys())
    if not valid_ids:
        return {"answer": state.get("answer", "")}

    if get_demo_mode():
        logger.info("[DEMO MODE] Skipping verification (demo mode)")
        return {"answer": state.get("answer", "")}

    llm = ChatOpenAI(model="gpt-4o-mini")
    messages = VERIFICATION_PROMPT.format_messages(
        valid_ids=", ".join(valid_ids),
        context=state.get("context", ""),
        answer=state.get("answer", ""),
    )
    response = llm.invoke(messages)
    cleaned = remove_invalid_citations(response.content or "", valid_ids)
    logger.info("Verification completed. Final citations: %s", ", ".join(extract_citation_ids(cleaned)))
    return {"answer": cleaned}


@lru_cache(maxsize=1)
def get_graph():
    graph = StateGraph(QAState)
    graph.add_node("retrieve", _retrieve_node)
    graph.add_node("answer", _answer_node)
    graph.add_node("verify", _verify_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", "verify")
    graph.add_edge("verify", END)

    return graph.compile()
