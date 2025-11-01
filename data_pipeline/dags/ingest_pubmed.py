"""
Airflow DAG for ingesting papers from PubMed
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.pubmed_ingester import ingest_pubmed_papers


default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ingest_pubmed',
    default_args=default_args,
    description='Ingest papers from PubMed API',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=days_ago(1),
    catchup=False,
    tags=['ingestion', 'pubmed'],
)

ingest_task = PythonOperator(
    task_id='ingest_pubmed_papers',
    python_callable=ingest_pubmed_papers,
    op_kwargs={
        'query': 'healthcare OR medical OR clinical',
        'max_results': 1000,
        'days_back': 1
    },
    dag=dag,
)

ingest_task

