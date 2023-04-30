# from sqlalchemy import create_engine
# import pandas as pd
# import json

# engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
# accident_df = pd.read_sql("""SELECT
#        (properties_vehicles :: json ->> 0) :: json  ->> 'year' as year,
#        (properties_vehicles :: json ->> 0) :: json  ->> 'brand' as brand,
#        (properties_vehicles :: json ->> 0) :: json  ->> 'color' as color,
#        (properties_vehicles :: json ->> 0) :: json  ->> 'model' as model,
#        (properties_vehicles :: json ->> 0) :: json  ->> 'category' as category,
#        (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'role' as role,
#        (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'gender' as gender,
#        (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'health_status' as health_status,
#        (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'years_of_driving_experience' as years_of_driving_experience,
#        (((properties_vehicles :: json ->> 0) :: json  ->> 'participants') :: json ->> 0) :: json  ->> 'violations' as violations
# FROM accident_dds ad;""", con=engine)


# print(accident_df)


from sqlalchemy import create_engine
import pandas as pd
import json

engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
accident_df = pd.read_sql("""SELECT
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
FROM accident_dds ad;""", con=engine)


print(accident_df)






