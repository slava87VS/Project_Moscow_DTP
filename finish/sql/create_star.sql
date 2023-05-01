-- таблица измерений
CREATE TABLE dds_1.moskow_dtp_dim (
dim_id serial PRIMARY KEY,
properties_id int8 UNIQUE,
properties_light text,
properties_region text,
properties_weather text,
properties_category text,
properties_severity text,
properties_road_conditions text,
brand text,
color text,
model text,
category text,
gender text,
year int8
);
-- таблица фактов
CREATE TABLE dds_1.moskow_dtp_fact (
dtp_id serial PRIMARY KEY,
properties_id int8,
years_of_driving_experience int8,
properties_participants_count int8,
CONSTRAINT fk_properties_id FOREIGN KEY (properties_id) REFERENCES dds_1.moskow_dtp_dim (properties_id)
);