"""
Script for syncing papers from OpenAlex API
"""
import requests
from typing import List, Dict, Optional
from loguru import logger
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def fetch_openalex_papers(
    filters: Optional[Dict] = None,
    max_results: int = 500,
    cursor: Optional[str] = None
) -> List[Dict]:
    """Fetch papers from OpenAlex API"""
    base_url = "https://api.openalex.org/works"
    
    params = {
        'per_page': min(max_results, 200),  # OpenAlex max per page
        'page': 1
    }
    
    if filters:
        # Convert filters to OpenAlex format
        filter_str = ','.join([f"{k}:{v}" for k, v in filters.items()])
        params['filter'] = filter_str
    
    try:
        papers = []
        page = 1
        
        while len(papers) < max_results:
            params['page'] = page
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                break
            
            for work in results:
                paper = {
                    'id': work.get('id'),
                    'title': work.get('title', ''),
                    'abstract': work.get('abstract', ''),
                    'authors': [author.get('author', {}).get('display_name', '') 
                               for author in work.get('authorships', [])],
                    'publication_date': work.get('publication_date'),
                    'doi': work.get('doi', ''),
                    'openalex_id': work.get('id'),
                    'concepts': [concept.get('display_name', '') 
                               for concept in work.get('concepts', [])],
                    'cited_by_count': work.get('cited_by_count', 0),
                    'is_open_access': work.get('open_access', {}).get('is_oa', False)
                }
                papers.append(paper)
                
                if len(papers) >= max_results:
                    break
            
            # Check if there are more pages
            meta = data.get('meta', {})
            if not meta.get('next_cursor') or len(papers) >= max_results:
                break
            
            page += 1
        
        logger.info(f"Fetched {len(papers)} papers from OpenAlex")
        return papers
        
    except Exception as e:
        logger.error(f"Error fetching OpenAlex papers: {str(e)}")
        raise


def save_papers_to_db(papers: List[Dict]):
    """Save papers to database"""
    # TODO: Implement database saving logic
    logger.info(f"Saving {len(papers)} papers to database")
    pass


def sync_openalex_papers(
    filters: Optional[Dict] = None,
    max_results: int = 500,
    cursor: Optional[str] = None
):
    """Main sync function"""
    logger.info("Starting OpenAlex sync")
    
    try:
        # Fetch papers from OpenAlex
        papers = fetch_openalex_papers(filters, max_results, cursor)
        
        if not papers:
            logger.warning("No papers fetched from OpenAlex")
            return
        
        # Save to database
        save_papers_to_db(papers)
        
        logger.info(f"Successfully synced {len(papers)} papers from OpenAlex")
        
    except Exception as e:
        logger.error(f"OpenAlex sync failed: {str(e)}")
        raise


if __name__ == "__main__":
    sync_openalex_papers(
        filters={
            'concepts.display_name': 'Medicine',
            'is_oa': True
        },
        max_results=100
    )

