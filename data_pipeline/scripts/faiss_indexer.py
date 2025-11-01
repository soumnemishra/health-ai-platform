"""
Script for indexing papers to FAISS vector database
"""
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()


def get_processed_papers(limit: int = None) -> List[Dict]:
    """Get processed papers from database"""
    # TODO: Implement database query
    logger.info(f"Fetching processed papers (limit: {limit})")
    return []


def generate_embeddings(texts: List[str], model: SentenceTransformer, batch_size: int = 32) -> np.ndarray:
    """Generate embeddings for texts"""
    logger.info(f"Generating embeddings for {len(texts)} texts")
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings


def create_faiss_index(embeddings: np.ndarray, dimension: int) -> faiss.Index:
    """Create FAISS index from embeddings"""
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype('float32'))
    logger.info(f"Created FAISS index with {index.ntotal} vectors")
    return index


def save_index(index: faiss.Index, filepath: str):
    """Save FAISS index to disk"""
    faiss.write_index(index, filepath)
    logger.info(f"Saved index to {filepath}")


def load_index(filepath: str) -> faiss.Index:
    """Load FAISS index from disk"""
    index = faiss.read_index(filepath)
    logger.info(f"Loaded index from {filepath}")
    return index


def index_papers_to_faiss(
    model_name: str = 'sentence-transformers/all-MiniLM-L6-v2',
    batch_size: int = 50,
    update_existing: bool = True
):
    """Main indexing function"""
    logger.info("Starting FAISS indexing")
    
    try:
        # Load model
        model = SentenceTransformer(model_name)
        dimension = model.get_sentence_embedding_dimension()
        logger.info(f"Loaded model: {model_name} (dimension: {dimension})")
        
        # Get processed papers
        papers = get_processed_papers()
        
        if not papers:
            logger.warning("No papers to index")
            return
        
        # Extract texts for embedding
        texts = []
        paper_ids = []
        for paper in papers:
            # Use title + abstract for embedding
            text = f"{paper.get('title', '')} {paper.get('abstract', '')}".strip()
            if text:
                texts.append(text)
                paper_ids.append(paper.get('id'))
        
        if not texts:
            logger.warning("No texts to embed")
            return
        
        # Generate embeddings
        embeddings = generate_embeddings(texts, model, batch_size)
        
        # Create or update index
        index_path = 'models/faiss_index.bin'
        
        if update_existing and os.path.exists(index_path):
            # Load existing index and add new vectors
            existing_index = load_index(index_path)
            existing_index.add(embeddings.astype('float32'))
            index = existing_index
            logger.info("Updated existing index")
        else:
            # Create new index
            index = create_faiss_index(embeddings, dimension)
        
        # Save index
        os.makedirs('models', exist_ok=True)
        save_index(index, index_path)
        
        # Save paper ID mapping
        # TODO: Save paper_ids mapping to database or file
        
        logger.info(f"Successfully indexed {len(texts)} papers")
        
    except Exception as e:
        logger.error(f"Indexing failed: {str(e)}")
        raise


if __name__ == "__main__":
    index_papers_to_faiss(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        batch_size=10,
        update_existing=False
    )

