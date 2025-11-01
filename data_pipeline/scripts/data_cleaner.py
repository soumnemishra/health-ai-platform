"""
Script for cleaning and normalizing paper data
"""
from typing import List, Dict
from loguru import logger
import re


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (optional)
    # text = re.sub(r'[^\w\s]', '', text)
    
    return text.strip()


def normalize_authors(authors: List[str]) -> List[str]:
    """Normalize author names"""
    normalized = []
    for author in authors:
        if author:
            # Basic normalization
            author = author.strip()
            normalized.append(author)
    return normalized


def extract_year_from_date(date_str: str) -> Optional[int]:
    """Extract year from date string"""
    if not date_str:
        return None
    
    # Try to extract year
    match = re.search(r'\d{4}', date_str)
    if match:
        return int(match.group())
    return None


def normalize_keywords(keywords: List[str]) -> List[str]:
    """Normalize keywords"""
    normalized = []
    for keyword in keywords:
        if keyword:
            keyword = keyword.strip().lower()
            if keyword:
                normalized.append(keyword)
    return list(set(normalized))  # Remove duplicates


def clean_paper(paper: Dict) -> Dict:
    """Clean a single paper"""
    cleaned = paper.copy()
    
    # Clean text fields
    if 'title' in cleaned:
        cleaned['title'] = clean_text(cleaned['title'])
    
    if 'abstract' in cleaned:
        cleaned['abstract'] = clean_text(cleaned['abstract'])
    
    if 'text' in cleaned:
        cleaned['text'] = clean_text(cleaned['text'])
    
    # Normalize authors
    if 'authors' in cleaned:
        cleaned['authors'] = normalize_authors(cleaned['authors'])
    
    # Normalize keywords
    if 'keywords' in cleaned:
        cleaned['keywords'] = normalize_keywords(cleaned['keywords'])
    
    # Extract year
    if 'publication_date' in cleaned:
        year = extract_year_from_date(cleaned['publication_date'])
        if year:
            cleaned['year'] = year
    
    return cleaned


def clean_papers(papers: List[Dict]) -> List[Dict]:
    """Clean multiple papers"""
    logger.info(f"Cleaning {len(papers)} papers")
    cleaned = []
    
    for paper in papers:
        try:
            cleaned_paper = clean_paper(paper)
            cleaned.append(cleaned_paper)
        except Exception as e:
            logger.error(f"Error cleaning paper {paper.get('id')}: {str(e)}")
            continue
    
    logger.info(f"Successfully cleaned {len(cleaned)} papers")
    return cleaned


if __name__ == "__main__":
    # Example usage
    sample_papers = [
        {
            'id': '1',
            'title': '  Sample  Title  ',
            'abstract': 'Sample abstract',
            'authors': ['Author One', 'Author Two'],
            'keywords': ['keyword1', 'keyword2', 'keyword1']
        }
    ]
    
    cleaned = clean_papers(sample_papers)
    print(cleaned)

