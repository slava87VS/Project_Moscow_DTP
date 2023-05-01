from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'create_data_mart',
    default_args=default_args,
    description='Create data mart table from source data',
    schedule_interval=timedelta(days=30),
)

def create_data_mart():
    engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
    data_mart = pd.read_sql("""SELECT mdd.properties_light, mdd.properties_region, mdd.properties_weather, 
           mdd.properties_category, mdd.properties_severity, mdd.properties_road_conditions, 
           mdd.brand, mdd.color, mdd.model, mdd.category, mdd.gender, mdd.year_car, 
           mdf.years_of_driving_experience, mdf.properties_participants_count
    FROM dds_1.moskow_dtp_dim mdd
    JOIN dds_1.moskow_dtp_fact mdf
    ON mdd.properties_id = mdf.properties_id;""", con=engine)
    data_mart.to_sql('data_mart', engine, schema='cdm', if_exists='replace', index=False, method='multi')
    engine.dispose()

create_data_mart_task = PythonOperator(
    task_id='create_data_mart',
    python_callable=create_data_mart,
    dag=dag,
)

create_data_mart_task
