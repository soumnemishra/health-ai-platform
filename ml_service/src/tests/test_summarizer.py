"""
Unit tests for summarization module
"""
import pytest
from src.summarizer.extractive_summarizer import ExtractiveSummarizer


@pytest.mark.asyncio
async def test_extractive_summarizer():
    """Test extractive summarization"""
    summarizer = ExtractiveSummarizer(method="lexrank", sentences_count=2)
    
    text = """
    Machine learning is a method of data analysis that automates analytical model building.
    It is a branch of artificial intelligence based on the idea that systems can learn from data,
    identify patterns and make decisions with minimal human intervention. Machine learning algorithms
    build mathematical models based on training data in order to make predictions or decisions
    without being explicitly programmed to do so.
    """
    
    summary = await summarizer.summarize(text)
    assert len(summary) > 0
    assert isinstance(summary, str)

