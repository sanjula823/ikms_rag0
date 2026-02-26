"""
Mock/Demo Pinecone vectorstore for testing without API keys.
Stores vectors in memory.
"""
from typing import Dict, List, Any
from dataclasses import dataclass
from langchain_core.documents import Document
import json


@dataclass
class MockVector:
    """In-memory vector storage"""
    id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any]


class MockVectorStore:
    """Mock Pinecone that stores vectors in memory"""
    
    def __init__(self):
        self.vectors: Dict[str, MockVector] = {}
        self.counter = 0
    
    def add_texts(self, texts: List[str], metadatas: List[Dict] = None, namespace: str = None) -> List[str]:
        """Add texts to the mock store"""
        ids = []
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        for text, metadata in zip(texts, metadatas):
            self.counter += 1
            vec_id = f"vec_{self.counter}"
            # Mock embedding: simple hash-based "vector"
            mock_embedding = [float(ord(c) % 10) / 10 for c in text[:1536]]
            
            self.vectors[vec_id] = MockVector(
                id=vec_id,
                text=text,
                embedding=mock_embedding,
                metadata=metadata
            )
            ids.append(vec_id)
        
        return ids
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Mock similarity search - returns top k most recent docs"""
        if not self.vectors:
            return []
        
        # Simple mock: return last k added (simulates relevance)
        all_docs = list(self.vectors.values())
        top_docs = all_docs[-k:] if len(all_docs) >= k else all_docs
        top_docs.reverse()  # Most recent first
        
        docs = []
        for doc in top_docs:
            docs.append(Document(
                page_content=doc.text,
                metadata=doc.metadata
            ))
        
        return docs
    
    def describe_index_stats(self):
        """Return mock index stats"""
        return {"total_vector_count": len(self.vectors)}


# Global mock store instance
_mock_store = MockVectorStore()


def get_mock_vectorstore() -> MockVectorStore:
    """Get the global mock vectorstore"""
    return _mock_store
