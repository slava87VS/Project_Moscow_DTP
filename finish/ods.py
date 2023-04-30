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



