from sqlalchemy import create_engine
import pandas as pd
import json

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
accident_df = pd.read_sql('select * from public.accident', con=engine)


# decode Unicode escape sequences in the 'properties_vehicles' column
accident_df['properties_vehicles'] = accident_df['properties_vehicles'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))
accident_df['properties_participants'] = accident_df['properties_participants'].apply(lambda x: x.encode('utf-8').decode('unicode_escape'))



accident_df.to_sql('accident_dds', engine, if_exists='replace', index=False, method='multi')

engine.dispose()

