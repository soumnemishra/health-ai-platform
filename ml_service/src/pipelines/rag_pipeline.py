"""
End-to-end RAG (Retrieval-Augmented Generation) pipeline
"""
from typing import List, Dict, Optional
from loguru import logger

from src.retrieval.hybrid_retriever import HybridRetriever
from src.reranker.cross_encoder import CrossEncoderReranker
from src.summarizer.abstractive_summarizer import AbstractiveSummarizer


class RAGPipeline:
    def __init__(
        self,
        retriever_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.retriever = HybridRetriever(model_name=retriever_model)
        self.reranker = CrossEncoderReranker(model_name=reranker_model)
        self.summarizer = AbstractiveSummarizer()
        self.documents = []
        logger.info("Initialized RAGPipeline")
    
    def load_documents(self, documents: List[str]):
        """Load and index documents"""
        self.documents = documents
        self.retriever.build_index(documents)
        logger.info(f"Loaded {len(documents)} documents")
    
    async def retrieve(
        self,
        query: str,
        filters: Optional[Dict] = None,
        limit: int = 10,
        use_reranker: bool = True
    ) -> List[Dict]:
        """Retrieve relevant documents"""
        # Initial retrieval (retrieve more than needed for reranking)
        initial_k = limit * 3 if use_reranker else limit
        
        results = self.retriever.retrieve(query, k=initial_k)
        
        # Rerank if enabled
        if use_reranker and len(results) > limit:
            documents = [r["document"] for r in results]
            reranked = self.reranker.rerank(query, documents, top_k=limit)
            
            # Map back to original results with reranked scores
            for i, rerank_result in enumerate(reranked):
                original = next(r for r in results if r["document"] == rerank_result["document"])
                original["rerank_score"] = rerank_result["score"]
                original["score"] = rerank_result["score"]  # Use reranked score
        
        return results[:limit]
    
    async def get_embedding(self, paper_id: str) -> Optional:
        """Get embedding for a paper (placeholder - needs implementation)"""
        # TODO: Implement embedding lookup by paper_id
        logger.warning(f"get_embedding not fully implemented for paper_id: {paper_id}")
        return None
    
    async def generate_answer(
        self,
        query: str,
        context: Optional[str] = None,
        retrieve_first: bool = True
    ) -> Dict:
        """Generate answer using retrieved context"""
        if retrieve_first:
            results = await self.retrieve(query, limit=3)
            context = "\n".join([r["document"] for r in results])
        
        if not context:
            return {"answer": "No relevant context found.", "context": ""}
        
        # Summarize the context
        summary = await self.summarizer.summarize(context, max_length=200)
        
        return {
            "answer": summary,
            "context": context,
            "sources": results if retrieve_first else []
        }

