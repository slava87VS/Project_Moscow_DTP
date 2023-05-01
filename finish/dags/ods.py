from sqlalchemy import create_engine
import pandas as pd
import json

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
accident_df = pd.read_sql('select * from stg.moskow_dtp', con=engine)


# decode Unicode escape sequences in the 'properties_vehicles' column
accident_df['properties_vehicles'] = accident_df['properties_vehicles'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
accident_df['properties_participants'] = accident_df['properties_participants'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
accident_df = accident_df.dropna()
accident_df.to_sql('moskow_dtp_ods', engine, schema='ods', if_exists='replace', index=False, method='multi')

engine.dispose()


engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
accident_df = pd.read_sql("""SELECT *,
       (properties_vehicles :: json ->> 0) :: json  ->> 'year' as year,
       (properties_vehicles :: json ->> 0) :: json  ->> 'brand' as brand,
       (properties_vehicles :: json ->> 0) :: json  ->> 'color' as color,
       (properties_vehicles :: json ->> 0) :: json  ->> 'model' as model,
       (properties_vehicles :: json ->> 0) :: json  ->> 'category' as category,
       (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'role' as role,
       (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'gender' as gender,
       (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'health_status' as health_status,
       (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'years_of_driving_experience' as years_of_driving_experience,
       (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'violations' as violations       
FROM ods.moskow_dtp_ods ad;""", con=engine)


accident_df.to_sql('moskow_dtp_ods', engine, schema='ods', if_exists='replace', index=False, method='multi')

engine.dispose()


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from datetime import timedelta
from sqlalchemy import create_engine
import pandas as pd
import json

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
    'ods_script_monthly',
    default_args=default_args,
    schedule_interval=timedelta(days=30)
)


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


def load_to_ods():
    accident_df = pd.read_sql('select * from stg.moskow_dtp', con=engine)

    # decode Unicode escape sequences in the 'properties_vehicles' column
    accident_df['properties_vehicles'] = accident_df['properties_vehicles'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
    accident_df['properties_participants'] = accident_df['properties_participants'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
    accident_df = accident_df.dropna()
    accident_df.to_sql('moskow_dtp_ods', engine, schema='ods', if_exists='replace', index=False, method='multi')


def transform_and_load():
    accident_df = pd.read_sql("""SELECT *,
           (properties_vehicles :: json ->> 0) :: json  ->> 'year' as year,
           (properties_vehicles :: json ->> 0) :: json  ->> 'brand' as brand,
           (properties_vehicles :: json ->> 0) :: json  ->> 'color' as color,
           (properties_vehicles :: json ->> 0) :: json  ->> 'model' as model,
           (properties_vehicles :: json ->> 0) :: json  ->> 'category' as category,
           (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'role' as role,
           (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'gender' as gender,
           (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'health_status' as health_status,
           (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'years_of_driving_experience' as years_of_driving_experience,
           (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'violations' as violations       
    FROM ods.moskow_dtp_ods ad;""", con=engine)

    accident_df.to_sql('moskow_dtp_ods', engine, schema='ods', if_exists='replace', index=False, method='multi')


load_script_task = PythonOperator(
    task_id='load_to_ods',
    python_callable=load_to_ods,
    dag=dag
)

transform_script_task = PythonOperator(
    task_id='transform_and_load',
    python_callable=transform_and_load,
    dag=dag
)

load_script_task >> transform_script_task

