"""
Abstractive summarization using transformer models
"""
from transformers import pipeline
from typing import Optional
from loguru import logger


class AbstractiveSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        try:
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                device=-1  # CPU by default, use 0 for GPU
            )
            logger.info(f"Initialized AbstractiveSummarizer with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load summarization model: {str(e)}")
            # Fallback to smaller model
            self.summarizer = pipeline("summarization", device=-1)
            logger.info("Using fallback summarization model")
    
    async def summarize(
        self, 
        text: str, 
        max_length: int = 150, 
        min_length: int = 30
    ) -> str:
        """Generate abstractive summary"""
        try:
            # Truncate if too long (model limits)
            max_input_length = 1024
            if len(text) > max_input_length:
                text = text[:max_input_length]
                logger.warning(f"Text truncated to {max_input_length} characters")
            
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            summary = result[0]["summary_text"]
            logger.info(f"Generated abstractive summary (length: {len(summary)})")
            return summary
        
        except Exception as e:
            logger.error(f"Abstractive summarization error: {str(e)}")
            raise

