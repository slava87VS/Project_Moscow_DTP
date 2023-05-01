from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 1),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'execute_script_monthly',
    default_args=default_args,
    schedule_interval=timedelta(days=30)
)

def execute_script():
    # установка параметров подключения
    db_config = {'user': 'postgres',
                 'pwd': 'b74c3e6',
                 'host': 'localhost',
                 'port': '5432',
                 'db': 'postgres'}

    # формирование строки соединения
    conn_str = f"postgresql://{db_config['user']}:{db_config['pwd']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"

    # создание объекта подключения к БД
    engine = create_engine(conn_str)

    # выполнение запроса
    with engine.connect() as conn:
        conn.execute("""
            TRUNCATE TABLE dds_1.moskow_dtp_dim CASCADE;
            INSERT INTO dds_1.moskow_dtp_dim (
                properties_id,
                properties_light,
                properties_region,
                properties_weather,
                properties_category,
                properties_severity,
                properties_road_conditions,
                brand,
                color,
                model,
                category,
                gender,
                year_car
            )
            SELECT
                properties_id,
                properties_light,
                properties_region,
                properties_weather,
                properties_category,
                properties_severity,
                properties_road_conditions,
                brand,
                color,
                model,
                category,
                gender,
                year :: int
            FROM ods.moskow_dtp_ods;
            TRUNCATE TABLE dds_1.moskow_dtp_fact CASCADE;
            INSERT INTO dds_1.moskow_dtp_fact (
                properties_id,
                years_of_driving_experience,
                properties_participants_count
            )
            SELECT
                properties_id,
                years_of_driving_experience :: int,
                properties_participants_count
            FROM ods.moskow_dtp_ods;
        """)

execute_script_task = PythonOperator(
    task_id='execute_script',
    python_callable=execute_script,
    dag=dag
)
execute_script_task