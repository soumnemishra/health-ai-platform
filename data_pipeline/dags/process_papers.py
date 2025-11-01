"""
Airflow DAG for processing ingested papers
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.paper_processor import process_papers


default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'process_papers',
    default_args=default_args,
    description='Process ingested papers (extract text, metadata, etc.)',
    schedule_interval='0 3 * * *',  # Daily at 3 AM (after ingestion)
    start_date=days_ago(1),
    catchup=False,
    tags=['processing', 'papers'],
)

extract_task = PythonOperator(
    task_id='extract_paper_content',
    python_callable=process_papers,
    op_kwargs={
        'batch_size': 100,
        'extract_text': True,
        'extract_metadata': True
    },
    dag=dag,
)

extract_task

