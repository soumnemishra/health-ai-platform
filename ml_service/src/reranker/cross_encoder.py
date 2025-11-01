"""
Cross-encoder reranker for fine-grained relevance scoring
"""
from sentence_transformers import CrossEncoder
from typing import List, Dict
from loguru import logger


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
        logger.info(f"Initialized CrossEncoderReranker with model: {model_name}")
    
    def rerank(self, query: str, documents: List[str], top_k: int = 10) -> List[Dict]:
        """
        Rerank documents based on query-document pairs
        """
        if not documents:
            return []
        
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]
        
        # Get scores from cross-encoder
        scores = self.model.predict(pairs)
        
        # Combine with documents and sort
        results = list(zip(documents, scores))
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k
        reranked = []
        for doc, score in results[:top_k]:
            reranked.append({
                "document": doc,
                "score": float(score)
            })
        
        logger.info(f"Reranked {len(documents)} documents, returning top {top_k}")
        return reranked

