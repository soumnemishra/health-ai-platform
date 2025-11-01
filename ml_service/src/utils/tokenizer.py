"""
Tokenizer utilities for text processing
"""
from transformers import AutoTokenizer
from typing import List
from loguru import logger


class Tokenizer:
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        logger.info(f"Initialized Tokenizer with model: {model_name}")
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text"""
        return self.tokenizer.tokenize(text)
    
    def encode(self, text: str, max_length: int = 512, truncation: bool = True):
        """Encode text to token IDs"""
        return self.tokenizer.encode(
            text,
            max_length=max_length,
            truncation=truncation,
            padding="max_length",
            return_tensors="pt"
        )
    
    def decode(self, token_ids):
        """Decode token IDs to text"""
        return self.tokenizer.decode(token_ids, skip_special_tokens=True)

