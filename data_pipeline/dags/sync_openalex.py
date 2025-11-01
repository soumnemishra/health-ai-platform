"""
Airflow DAG for syncing papers from OpenAlex
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.openalex_syncer import sync_openalex_papers


default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'sync_openalex',
    default_args=default_args,
    description='Sync papers from OpenAlex API',
    schedule_interval='0 1 * * *',  # Daily at 1 AM
    start_date=days_ago(1),
    catchup=False,
    tags=['ingestion', 'openalex'],
)

sync_task = PythonOperator(
    task_id='sync_openalex_papers',
    python_callable=sync_openalex_papers,
    op_kwargs={
        'filters': {
            'concepts.display_name': 'Medicine',
            'is_oa': True
        },
        'max_results': 500,
        'cursor': None
    },
    dag=dag,
)

sync_task

