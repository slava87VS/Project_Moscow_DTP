from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd
import json
import urllib.request
from psycopg2.extensions import register_adapter, AsIs


def adapt_dict(dict_obj):
    return AsIs(json.dumps(dict_obj))


register_adapter(dict, adapt_dict)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'load_moskow_dtp_data',
    default_args=default_args,
    description='Load Moskow DTP data into PostgreSQL database',
    schedule_interval='@monthly',
)

def load_data_to_postgres():
    url = 'https://cms.dtp-stat.ru/media/opendata/moskva.geojson'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    df = pd.json_normalize(data['features'])

    df = df.rename(columns={'type': 'type',
                            'geometry.type': 'geometry_type',
                            'geometry.coordinates': 'geometry_coordinates',
                            'properties.id': 'properties_id',
                            'properties.tags': 'properties_tags',
                            'properties.light': 'properties_light',
                            'properties.point.lat': 'properties_point_lat',
                            'properties.point.long': 'properties_point_long',
                            'properties.nearby': 'properties_nearby',
                            'properties.region': 'properties_region',
                            'properties.scheme': 'properties_scheme',
                            'properties.address': 'properties_address',
                            'properties.weather': 'properties_weather',
                            'properties.category': 'properties_category',
                            'properties.datetime': 'properties_datetime',
                            'properties.severity': 'properties_severity',
                            'properties.vehicles': 'properties_vehicles',
                            'properties.dead_count': 'properties_dead_count',
                            'properties.participants': 'properties_participants',
                            'properties.injured_count': 'properties_injured_count',
                            'properties.parent_region': 'properties_parent_region',
                            'properties.road_conditions': 'properties_road_conditions',
                            'properties.participants_count': 'properties_participants_count',
                            'properties.participant_categories': 'properties_participant_categories'})

    
    df['properties_vehicles'] = df['properties_vehicles'].apply(json.dumps)
    df['properties_participants'] = df['properties_participants'].apply(json.dumps)
    df['properties_point_long'] = df['properties_point_long'].astype(float)

    engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
    df.to_sql('moskow_dtp', engine, schema='stg', if_exists='replace', index=False, method='multi')
    engine.dispose()

with dag:
    load_data = PythonOperator(
        task_id='load_data_to_postgres',
        python_callable=load_data_to_postgres
    )
    
load_data
