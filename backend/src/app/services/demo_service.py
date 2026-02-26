"""
Demo/Mock services that work without API keys
"""
import os
from typing import Dict, List
from langchain_core.documents import Document
from app.utils.logging import get_logger

logger = get_logger(__name__)


def get_demo_mode() -> bool:
    """Check if demo mode is enabled"""
    return os.getenv("DEMO_MODE", "false").lower() == "true"


def mock_retrieve_chunks(question: str, top_k: int) -> List[Document]:
    """Mock retrieval without Pinecone"""
    logger.info(f"[DEMO] Retrieving {top_k} mock chunks for: {question}")
    
    # Mock response chunks
    mock_chunks = [
        Document(
            page_content="Machine learning is a subset of artificial intelligence that focuses on the ability of computers to learn from data without being explicitly programmed. It uses algorithms and statistical models to identify patterns and make predictions based on input data.",
            metadata={"page": 1, "source": "ai_basics.pdf"}
        ),
        Document(
            page_content="Neural networks are computational models inspired by biological neural networks found in animal brains. They consist of interconnected nodes (neurons) organized in layers that process information through weighted connections.",
            metadata={"page": 2, "source": "ai_basics.pdf"}
        ),
        Document(
            page_content="Deep learning is a specialized subset of machine learning that uses neural networks with multiple layers (hence 'deep'). These networks can automatically discover representations needed for detection or classification from raw input.",
            metadata={"page": 3, "source": "ai_basics.pdf"}
        ),
        Document(
            page_content="Vector embeddings are numerical representations of text where words or documents are mapped to points in a multidimensional space. Similar concepts have vectors that are close to each other in this space.",
            metadata={"page": 4, "source": "ai_basics.pdf"}
        ),
    ]
    
    return mock_chunks[:top_k]


def mock_qa_response(question: str, context: str, top_k: int) -> Dict:
    """Mock Q&A response without OpenAI"""
    logger.info(f"[DEMO] Generating mock Q&A for: {question}")
    
    # Generate a simple mock answer based on question
    question_lower = question.lower()
    
    if "neural network" in question_lower or "network" in question_lower:
        answer = "Neural networks are computational models inspired by biological neurons [C1]. They consist of interconnected nodes organized in layers that process information through weighted connections [C2]. Modern deep neural networks can have many layers to learn complex patterns [C3]."
    elif "machine learning" in question_lower:
        answer = "Machine learning is a subset of artificial intelligence that enables computers to learn from data [C1]. It uses algorithms to identify patterns and make predictions without explicit programming [C2]. This includes supervised, unsupervised, and reinforcement learning approaches."
    elif "embedding" in question_lower:
        answer = "Vector embeddings are numerical representations where text or concepts are mapped to points in multidimensional space [C1]. Similar items have vectors that are close together [C2]."
    else:
        answer = f"Based on the search context, here's what I found about your question: {question[:50]}... [C1][C2] The system retrieved relevant information that addresses your inquiry."
    
    # Mock citations
    citations = {
        "C1": {
            "page": 1,
            "snippet": "Machine learning is a subset of artificial intelligence...",
            "source": "ai_basics.pdf"
        },
        "C2": {
            "page": 2,
            "snippet": "Neural networks are computational models...",
            "source": "ai_basics.pdf"
        },
        "C3": {
            "page": 3,
            "snippet": "Deep learning uses neural networks with multiple layers...",
            "source": "ai_basics.pdf"
        }
    }
    
    return {
        "answer": answer,
        "context": "[C1] Sample context...\n[C2] More context...",
        "citations": citations
    }


def mock_search_response(query: str, top_k: int) -> Dict:
    """Mock search response without Pinecone"""
    logger.info(f"[DEMO] Generating mock search results for: {query}")
    
    mock_results = [
        {
            "content": "Machine learning is a subset of artificial intelligence that focuses on the ability of computers to learn from data without being explicitly programmed.",
            "page": 1,
            "source": "ai_basics.pdf",
            "score": 0.95
        },
        {
            "content": "Neural networks are computational models inspired by biological neural networks found in animal brains.",
            "page": 2,
            "source": "ai_basics.pdf",
            "score": 0.88
        },
        {
            "content": "Deep learning uses neural networks with multiple layers to discover representations automatically.",
            "page": 3,
            "source": "ai_basics.pdf",
            "score": 0.82
        },
        {
            "content": "Vector embeddings map concepts to points in multidimensional space where similar items cluster together.",
            "page": 4,
            "source": "ai_basics.pdf",
            "score": 0.78
        },
        {
            "content": "Supervised learning uses labeled data to train models to make predictions or classifications.",
            "page": 5,
            "source": "ai_basics.pdf",
            "score": 0.75
        }
    ]
    
    return {
        "query": query,
        "results": mock_results[:top_k],
        "count": min(len(mock_results), top_k)
    }


def mock_index_pdf(file_path: str = None, file_bytes: bytes = None, filename: str = "document.pdf") -> Dict:
    """Mock PDF indexing without Pinecone"""
    if file_path:
        logger.info(f"[DEMO] Mock indexing PDF from path: {file_path}")
        chunks = 10
        pages = 5
        source = "sample.pdf"
    else:
        logger.info(f"[DEMO] Mock indexing uploaded PDF: {filename}")
        # Mock: simulate chunking based on file size
        chunks = max(3, (len(file_bytes) // 1000) if file_bytes else 5)
        pages = max(1, chunks // 2)
        source = filename
    
    return {
        "chunks_indexed": chunks,
        "source": source,
        "pages": pages
    }
