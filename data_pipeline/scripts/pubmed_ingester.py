"""
PubMed Ingestion Script
Fetches PubMed articles via NCBI E-utilities and upserts them into Supabase.
"""
import os
import sys
import time
import xml.etree.ElementTree as ET
from typing import List, Dict
import requests
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Environment variables
NCBI_API_KEY = os.getenv("NCBI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
PUBMED_DEFAULT_QUERY = os.getenv("PUBMED_DEFAULT_QUERY", "")

# NCBI E-utilities base URLs
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Batch size for efetch
BATCH_SIZE = 200
# Rate limit: 0.34 seconds per batch (allows ~3 requests/second)
RATE_LIMIT_DELAY = 0.34


def esearch(query: str) -> tuple[int, str, str]:
    """
    Step 1: Use esearch.fcgi to get Count, WebEnv, and QueryKey.
    
    Returns:
        tuple: (count, webenv, query_key)
    """
    params = {
        'db': 'pubmed',
        'term': query,
        'usehistory': 'y',
        'retmax': '0',
        'retmode': 'xml'
    }
    
    if NCBI_API_KEY:
        params['api_key'] = NCBI_API_KEY
    
    print(f"Step 1: Searching PubMed for query: '{query}'")
    response = requests.get(ESEARCH_URL, params=params)
    response.raise_for_status()
    
    # Parse XML response
    root = ET.fromstring(response.content)
    
    # Extract Count, WebEnv, QueryKey
    count_elem = root.find('.//Count')
    webenv_elem = root.find('.//WebEnv')
    query_key_elem = root.find('.//QueryKey')
    
    count = int(count_elem.text) if count_elem is not None and count_elem.text else 0
    webenv = webenv_elem.text if webenv_elem is not None else ""
    query_key = query_key_elem.text if query_key_elem is not None else ""
    
    print(f"  Found {count} articles")
    print(f"  WebEnv: {webenv[:50]}...")
    print(f"  QueryKey: {query_key}")
    
    if not webenv or not query_key:
        raise ValueError("Failed to get WebEnv or QueryKey from esearch response")
    
    return count, webenv, query_key


def efetch_batch(webenv: str, query_key: str, retstart: int, retmax: int = BATCH_SIZE) -> str:
    """
    Fetch a batch of articles using efetch.fcgi.
    
    Args:
        webenv: WebEnv from esearch
        query_key: QueryKey from esearch
        retstart: Starting position
        retmax: Number of records to fetch
    
    Returns:
        str: Raw XML response
    """
    params = {
        'db': 'pubmed',
        'query_key': query_key,
        'WebEnv': webenv,
        'retstart': str(retstart),
        'retmax': str(retmax),
        'retmode': 'xml'
    }
    
    if NCBI_API_KEY:
        params['api_key'] = NCBI_API_KEY
    
    response = requests.get(EFETCH_URL, params=params)
    response.raise_for_status()
    
    return response.text


def extract_articles(xml_content: str) -> List[Dict]:
    """
    Extract PMID and raw XML for each PubmedArticle.
    
    Args:
        xml_content: Raw XML string from efetch
    
    Returns:
        List of dicts with 'pmid', 'raw_xml', and 'source' keys
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"  Warning: XML parse error: {e}")
        return []
    
    articles = []
    
    # Find all PubmedArticle elements
    for article_elem in root.findall('.//PubmedArticle'):
        # Extract PMID
        pmid_elem = article_elem.find('.//PMID')
        if pmid_elem is not None and pmid_elem.text:
            pmid = pmid_elem.text.strip()
            
            # Convert article element to string
            raw_xml = ET.tostring(article_elem, encoding='unicode')
            
            articles.append({
                'pmid': pmid,
                'raw_xml': raw_xml,
                'source': 'pubmed'
            })
    
    return articles


def upsert_to_supabase(articles: List[Dict]):
    """
    Upsert articles into Supabase raw_pubmed_articles table.
    
    Args:
        articles: List of article dicts with pmid, raw_xml, source
    """
    if not articles:
        return
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    print(f"  Upserting {len(articles)} articles to Supabase...")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    try:
        result = supabase.table("raw_pubmed_articles").upsert(
            articles,
            on_conflict="pmid"
        ).execute()
        
        print(f"  Successfully upserted {len(articles)} articles")
    except Exception as e:
        print(f"  Error upserting to Supabase: {e}")
        raise


def main(query: str = None):
    """
    Main function to fetch PubMed articles and upsert to Supabase.
    
    Args:
        query: PubMed search query (defaults to PUBMED_DEFAULT_QUERY env var)
    """
    # Use provided query or default from env
    if query is None:
        query = PUBMED_DEFAULT_QUERY
    
    if not query:
        print("Error: No query provided. Use command-line argument or set PUBMED_DEFAULT_QUERY env var.")
        sys.exit(1)
    
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        sys.exit(1)
    
    print("=" * 60)
    print("PubMed Ingestion Script")
    print("=" * 60)
    print(f"Query: {query}")
    print(f"Supabase URL: {SUPABASE_URL}")
    print()
    
    try:
        # Step 1: esearch to get Count, WebEnv, QueryKey
        count, webenv, query_key = esearch(query)
        
        if count == 0:
            print("No articles found for this query.")
            return
        
        print()
        print(f"Step 2: Fetching articles in batches of {BATCH_SIZE}...")
        
        total_upserted = 0
        
        # Step 2: Loop through efetch in batches
        for retstart in range(0, count, BATCH_SIZE):
            batch_num = (retstart // BATCH_SIZE) + 1
            total_batches = (count + BATCH_SIZE - 1) // BATCH_SIZE
            
            print(f"  Batch {batch_num}/{total_batches} (articles {retstart + 1}-{min(retstart + BATCH_SIZE, count)})...")
            
            # Fetch batch
            xml_content = efetch_batch(webenv, query_key, retstart, BATCH_SIZE)
            
            # Extract articles
            articles = extract_articles(xml_content)
            
            if articles:
                # Upsert to Supabase
                upsert_to_supabase(articles)
                total_upserted += len(articles)
            else:
                print(f"  Warning: No articles extracted from batch")
            
            # Rate limiting: sleep between batches (except after last batch)
            if retstart + BATCH_SIZE < count:
                time.sleep(RATE_LIMIT_DELAY)
        
        print()
        print("=" * 60)
        print(f"Completed! Total articles upserted: {total_upserted}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Get query from command-line argument or use default
    query_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(query_arg)
