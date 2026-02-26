from app.core.agents.agents import get_graph
from app.services.demo_service import get_demo_mode, mock_qa_response
from app.utils.logging import get_logger


logger = get_logger(__name__)


def run_qa(question: str, top_k: int = 4) -> dict:
    # Check if demo mode is enabled
    if get_demo_mode():
        logger.info("[DEMO MODE] Using mock Q&A service")
        return mock_qa_response(question, "", top_k)
    
    # Production mode: use real graph
    graph = get_graph()
    result = graph.invoke({"question": question, "top_k": top_k})
    response = {
        "answer": result.get("answer", ""),
        "context": result.get("context", ""),
        "citations": result.get("citations"),
    }
    logger.info("QA response ready")
    return response
