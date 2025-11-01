"""
Hybrid retrieval combining BM25 (sparse) and dense vector search
"""
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, Dict
from loguru import logger


class HybridRetriever:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.bm25_index = None
        self.dense_model = SentenceTransformer(model_name)
        self.faiss_index = None
        self.documents = []
        logger.info(f"Initialized HybridRetriever with model: {model_name}")
    
    def build_index(self, documents: List[str]):
        """Build both BM25 and FAISS indices"""
        self.documents = documents
        
        # Build BM25 index
        tokenized_docs = [doc.split() for doc in documents]
        self.bm25_index = BM25Okapi(tokenized_docs)
        logger.info(f"Built BM25 index for {len(documents)} documents")
        
        # Build dense embeddings and FAISS index
        embeddings = self.dense_model.encode(documents, show_progress_bar=True)
        dimension = embeddings.shape[1]
        
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(embeddings.astype('float32'))
        logger.info(f"Built FAISS index with dimension {dimension}")
    
    def retrieve(self, query: str, k: int = 10, alpha: float = 0.5) -> List[Dict]:
        """
        Hybrid retrieval combining BM25 and dense search
        alpha: weight for dense score (1-alpha for BM25)
        """
        if self.bm25_index is None or self.faiss_index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # BM25 retrieval
        tokenized_query = query.split()
        bm25_scores = self.bm25_index.get_scores(tokenized_query)
        bm25_scores = self._normalize_scores(bm25_scores)
        
        # Dense retrieval
        query_embedding = self.dense_model.encode([query])
        distances, indices = self.faiss_index.search(query_embedding.astype('float32'), k)
        dense_scores = self._normalize_scores(1 / (1 + distances[0]))  # Convert distance to similarity
        
        # Combine scores
        combined_scores = alpha * dense_scores + (1 - alpha) * bm25_scores
        
        # Get top k results
        top_indices = np.argsort(combined_scores)[::-1][:k]
        
        results = []
        for idx in top_indices:
            results.append({
                "document": self.documents[idx],
                "score": float(combined_scores[idx]),
                "bm25_score": float(bm25_scores[idx]),
                "dense_score": float(dense_scores[idx] if idx < len(dense_scores) else 0)
            })
        
        return results
    
    def _normalize_scores(self, scores: np.ndarray) -> np.ndarray:
        """Normalize scores to [0, 1] range"""
        min_score = scores.min()
        max_score = scores.max()
        if max_score == min_score:
            return np.ones_like(scores)
        return (scores - min_score) / (max_score - min_score)

