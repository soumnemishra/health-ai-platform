"""
Vector database utilities for embeddings
"""
import faiss
import numpy as np
from typing import List, Optional
from loguru import logger


class VectorDB:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_doc = {}
        logger.info(f"Initialized VectorDB with dimension {dimension}")
    
    def add_documents(self, embeddings: np.ndarray, doc_ids: List[str]):
        """Add documents to vector database"""
        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} != {self.dimension}")
        
        self.index.add(embeddings.astype('float32'))
        
        start_id = len(self.id_to_doc)
        for i, doc_id in enumerate(doc_ids):
            self.id_to_doc[start_id + i] = doc_id
        
        logger.info(f"Added {len(doc_ids)} documents to vector DB")
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[dict]:
        """Search for similar documents"""
        if query_embedding.shape[1] != self.dimension:
            raise ValueError(f"Query dimension {query_embedding.shape[1]} != {self.dimension}")
        
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx in self.id_to_doc:
                results.append({
                    "doc_id": self.id_to_doc[idx],
                    "distance": float(distances[0][i]),
                    "score": 1 / (1 + float(distances[0][i]))  # Convert to similarity
                })
        
        return results
    
    def save(self, filepath: str):
        """Save index to disk"""
        faiss.write_index(self.index, filepath)
        logger.info(f"Saved index to {filepath}")
    
    def load(self, filepath: str):
        """Load index from disk"""
        self.index = faiss.read_index(filepath)
        logger.info(f"Loaded index from {filepath}")

