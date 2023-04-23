import json
import pandas as pd
import urllib.request
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter, AsIs


def adapt_dict(dict_obj):
    return AsIs(json.dumps(dict_obj))


register_adapter(dict, adapt_dict)

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

df = df.head(7)
df['properties_vehicles'] = df['properties_vehicles'].apply(json.dumps)
df['properties_participants'] = df['properties_participants'].apply(json.dumps)
df['properties_point_long'] = df['properties_point_long'].astype(float)

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')


df.to_sql('accident', engine, if_exists='replace', index=False, method='multi')

engine.dispose()
