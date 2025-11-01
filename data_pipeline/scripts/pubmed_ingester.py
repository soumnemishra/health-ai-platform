"""
Script for ingesting papers from PubMed API
"""
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_pubmed_ids(query: str, max_results: int = 1000) -> List[str]:
    """Fetch PubMed IDs for a given query"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': max_results,
        'retmode': 'json',
        'sort': 'pub_date',
        'order': 'desc'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        pmids = data.get('esearchresult', {}).get('idlist', [])
        logger.info(f"Fetched {len(pmids)} PubMed IDs for query: {query}")
        return pmids
    except Exception as e:
        logger.error(f"Error fetching PubMed IDs: {str(e)}")
        raise


def fetch_paper_details(pmids: List[str]) -> List[Dict]:
    """Fetch detailed information for PubMed IDs"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    params = {
        'db': 'pubmed',
        'id': ','.join(pmids),
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse XML response (simplified - use BioPython for full parsing)
        papers = []
        logger.info(f"Fetched details for {len(pmids)} papers")
        
        # TODO: Parse XML and extract paper details
        # This is a placeholder - implement full XML parsing
        
        return papers
    except Exception as e:
        logger.error(f"Error fetching paper details: {str(e)}")
        raise


def save_papers_to_db(papers: List[Dict]):
    """Save papers to database"""
    # TODO: Implement database saving logic
    logger.info(f"Saving {len(papers)} papers to database")
    pass


def ingest_pubmed_papers(
    query: str,
    max_results: int = 1000,
    days_back: int = 1
):
    """Main ingestion function"""
    logger.info(f"Starting PubMed ingestion for query: {query}")
    
    try:
        # Fetch PubMed IDs
        pmids = fetch_pubmed_ids(query, max_results)
        
        if not pmids:
            logger.warning("No papers found for query")
            return
        
        # Fetch paper details
        papers = fetch_paper_details(pmids)
        
        # Save to database
        save_papers_to_db(papers)
        
        logger.info(f"Successfully ingested {len(papers)} papers")
        
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise


if __name__ == "__main__":
    ingest_pubmed_papers(
        query="healthcare OR medical OR clinical",
        max_results=100,
        days_back=1
    )

