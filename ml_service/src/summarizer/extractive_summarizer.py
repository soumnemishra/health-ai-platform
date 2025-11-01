"""
Extractive summarization using sentence ranking
"""
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from typing import Optional
from loguru import logger


class ExtractiveSummarizer:
    def __init__(self, method: str = "lexrank", sentences_count: int = 5):
        self.method = method
        self.sentences_count = sentences_count
        
        if method == "lexrank":
            self.summarizer = LexRankSummarizer()
        elif method == "lsa":
            self.summarizer = LsaSummarizer()
        else:
            raise ValueError(f"Unknown method: {method}")
        
        logger.info(f"Initialized ExtractiveSummarizer with method: {method}")
    
    async def summarize(self, text: str, sentences_count: Optional[int] = None) -> str:
        """Generate extractive summary"""
        if sentences_count is None:
            sentences_count = self.sentences_count
        
        try:
            # Parse text
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            
            # Generate summary
            summary_sentences = self.summarizer(parser.document, sentences_count)
            
            # Join sentences
            summary = " ".join(str(sentence) for sentence in summary_sentences)
            
            logger.info(f"Generated extractive summary with {len(summary_sentences)} sentences")
            return summary
        
        except Exception as e:
            logger.error(f"Extractive summarization error: {str(e)}")
            raise

