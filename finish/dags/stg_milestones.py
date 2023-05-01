from datetime import datetime, timedelta
import json
import pandas as pd
import urllib.request
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter, AsIs
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'monthly_data_load',
    default_args=default_args,
    schedule_interval='@monthly',
    catchup=False
)

def load_milestones():
    milestones = pd.read_csv(r'C:\Users\adm\Desktop\Project_Moscow_DTP\finish\data\milestones.csv', sep=';')
    engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
    milestones.to_sql('milestones', engine, schema='stg', if_exists='replace', index=False, method='multi')
    engine.dispose()

load_milestones_task = PythonOperator(
    task_id='load_milestones',
    python_callable=load_milestones,
    dag=dag
)
