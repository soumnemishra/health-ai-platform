# Health AI Platform - Data Pipeline

Data ingestion and indexing pipeline for the Health AI Platform using Airflow or Prefect.

## Tech Stack

- **Apache Airflow** - Workflow orchestration
- **Prefect** - Alternative workflow orchestration
- **PubMed API** - Paper ingestion
- **OpenAlex API** - Alternative paper source
- **FAISS** - Vector indexing
- **Sentence Transformers** - Embedding generation

## Project Structure

```
data_pipeline/
├── dags/                     # Airflow DAGs or Prefect flows
│   ├── ingest_pubmed.py      # PubMed ingestion DAG
│   ├── process_papers.py     # Paper processing DAG
│   ├── index_to_faiss.py     # FAISS indexing DAG
│   └── sync_openalex.py      # OpenAlex sync DAG
├── scripts/                   # One-off scripts (data cleaning, reindexing)
│   ├── pubmed_ingester.py
│   ├── paper_processor.py
│   ├── faiss_indexer.py
│   ├── openalex_syncer.py
│   └── data_cleaner.py
├── configs/                   # Pipeline configs (sources, weights, thresholds)
│   ├── pipeline_config.yaml
│   ├── sources_config.yaml
│   └── thresholds_config.yaml
├── notebooks/                 # Exploratory Jupyter notebooks
│   └── exploratory_analysis.ipynb
└── requirements.txt
```

## Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Airflow (if using Airflow)**
   ```bash
   airflow db init
   airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
   ```

4. **Create `.env` file**
   ```env
   DATABASE_URL=mongodb://localhost:27017/health_ai
   PUBMED_API_KEY=your_api_key_here
   ```

5. **Copy DAGs to Airflow DAGs folder**
   ```bash
   cp -r dags/ /path/to/airflow/dags/
   ```

## DAGs

### Ingest PubMed
- **Schedule**: Daily at 2 AM
- **Description**: Fetches new papers from PubMed API
- **Tasks**: Fetch IDs, get details, save to database

### Process Papers
- **Schedule**: Daily at 3 AM (after ingestion)
- **Description**: Processes ingested papers (extract text, metadata, keywords)
- **Tasks**: Extract content, extract metadata, calculate scores

### Index to FAISS
- **Schedule**: Daily at 4 AM (after processing)
- **Description**: Generates embeddings and indexes papers to FAISS
- **Tasks**: Generate embeddings, create/update FAISS index

### Sync OpenAlex
- **Schedule**: Daily at 1 AM
- **Description**: Syncs papers from OpenAlex API
- **Tasks**: Fetch papers, save to database

## Scripts

### pubmed_ingester.py
Ingests papers from PubMed API. Can be run standalone or as part of DAG.

### paper_processor.py
Processes ingested papers: extracts text, metadata, keywords, calculates scores.

### faiss_indexer.py
Generates embeddings using sentence transformers and indexes to FAISS.

### openalex_syncer.py
Syncs papers from OpenAlex API (alternative to PubMed).

### data_cleaner.py
Cleans and normalizes paper data.

## Configuration

### pipeline_config.yaml
Main pipeline configuration including sources, processing, indexing settings.

### sources_config.yaml
Data source configuration (PubMed, OpenAlex, etc.) with rate limits and defaults.

### thresholds_config.yaml
Thresholds and weights for scoring, quality checks, indexing.

## Usage

### Running DAGs

**Airflow UI:**
1. Start Airflow: `airflow webserver` and `airflow scheduler`
2. Access UI at `http://localhost:8080`
3. Enable and trigger DAGs from UI

**Command line:**
```bash
airflow dags trigger ingest_pubmed
```

### Running Scripts Standalone

```bash
python scripts/pubmed_ingester.py
python scripts/paper_processor.py
python scripts/faiss_indexer.py
```

## Development

### Testing
```bash
pytest tests/
```

### Notebooks
```bash
jupyter lab notebooks/
```

## Notes

- DAGs use placeholder database operations - implement actual database logic
- PubMed ingestion requires API key (optional but recommended)
- FAISS indexing can be memory-intensive for large datasets
- Consider using Prefect instead of Airflow for modern workflow management

