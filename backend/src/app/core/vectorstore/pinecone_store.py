import os

from app.utils.logging import get_logger


logger = get_logger(__name__)


def get_vectorstore():
    """Get or create Pinecone vectorstore"""
    # Check if demo mode is enabled (MUST CHECK FIRST)
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    
    if demo_mode:
        logger.info("[DEMO MODE] Using mock vectorstore")
        from app.core.vectorstore.mock_store import get_mock_vectorstore
        return get_mock_vectorstore()
    
    # Only import Pinecone dependencies if NOT in demo mode
    try:
        from langchain_openai import OpenAIEmbeddings
        from langchain_pinecone import PineconeVectorStore
        from pinecone import Pinecone
    except ImportError as e:
        logger.error("Pinecone libraries not installed: %s", e)
        raise RuntimeError("langchain-pinecone must be installed for production mode. Use DEMO_MODE=true for testing.")
    
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")
    if not api_key or not index_name:
        raise RuntimeError("PINECONE_API_KEY and PINECONE_INDEX must be set")

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    client = Pinecone(api_key=api_key)
    index = client.Index(index_name)

    logger.info("Connected to Pinecone index %s", index_name)
    return PineconeVectorStore(index=index, embedding=embeddings, text_key="text")
