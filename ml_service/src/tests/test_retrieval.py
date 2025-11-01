"""
Unit tests for retrieval module
"""
import pytest
from src.retrieval.hybrid_retriever import HybridRetriever


def test_hybrid_retriever_initialization():
    """Test retriever initialization"""
    retriever = HybridRetriever()
    assert retriever.bm25_index is None
    assert retriever.faiss_index is None


def test_hybrid_retriever_build_index():
    """Test index building"""
    retriever = HybridRetriever()
    documents = [
        "This is a test document about machine learning.",
        "Another document about natural language processing.",
        "A third document about healthcare AI."
    ]
    retriever.build_index(documents)
    
    assert retriever.bm25_index is not None
    assert retriever.faiss_index is not None
    assert len(retriever.documents) == 3


def test_hybrid_retriever_retrieve():
    """Test retrieval"""
    retriever = HybridRetriever()
    documents = [
        "Machine learning is a subset of artificial intelligence.",
        "Natural language processing helps computers understand text.",
        "Healthcare AI can improve patient outcomes."
    ]
    retriever.build_index(documents)
    
    results = retriever.retrieve("machine learning", k=2)
    
    assert len(results) == 2
    assert "score" in results[0]
    assert "document" in results[0]


if __name__ == "__main__":
    pytest.main([__file__])

