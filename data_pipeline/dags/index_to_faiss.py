"""
Airflow DAG for indexing papers to FAISS vector database
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.faiss_indexer import index_papers_to_faiss


default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=15),
}

dag = DAG(
    'index_to_faiss',
    default_args=default_args,
    description='Index processed papers to FAISS vector database',
    schedule_interval='0 4 * * *',  # Daily at 4 AM (after processing)
    start_date=days_ago(1),
    catchup=False,
    tags=['indexing', 'faiss', 'vectors'],
)

index_task = PythonOperator(
    task_id='index_papers',
    python_callable=index_papers_to_faiss,
    op_kwargs={
        'model_name': 'sentence-transformers/all-MiniLM-L6-v2',
        'batch_size': 50,
        'update_existing': True
    },
    dag=dag,
)

index_task

