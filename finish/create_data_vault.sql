-- создание таблицы "vehicle" в хранилище "hub"
CREATE TABLE dds.hub_vehicle (
    vehicle_id INT PRIMARY KEY,
    brand TEXT,
    color TEXT,
    model TEXT,
    category TEXT
);
-- создание таблицы "driver" в хранилище "hub"
CREATE TABLE dds.hub_driver (
    driver_id INT PRIMARY KEY,
    gender TEXT,
    years_of_driving_experience INT
);
CREATE TABLE dds.hub_accident (
    accident_id INT PRIMARY KEY
);
-- создание таблицы "accident_vehicle" в хранилище "link"
CREATE TABLE dds.link_accident_vehicle (
accident_id INT,
vehicle_id INT,
PRIMARY KEY (accident_id, vehicle_id),
FOREIGN KEY (accident_id) REFERENCES dds.hub_accident (accident_id),
FOREIGN KEY (vehicle_id) REFERENCES dds.hub_vehicle (vehicle_id)
);
-- создание таблицы "accident_driver" в хранилище "link"
CREATE TABLE dds.link_accident_driver (
accident_id INT,
driver_id INT,
PRIMARY KEY (accident_id, driver_id),
FOREIGN KEY (accident_id) REFERENCES dds.hub_accident (accident_id),
FOREIGN KEY (driver_id) REFERENCES dds.hub_driver (driver_id)
);
-- создание таблицы "accident_properties" в хранилище "satellite"
CREATE TABLE dds.satellite_accident_properties (
    accident_id INT,
    properties_light TEXT,
    properties_nearby TEXT,
    properties_region TEXT,
    properties_scheme TEXT,
    properties_weather TEXT,
    properties_category TEXT,
    properties_severity TEXT,
    properties_road_conditions TEXT,
    properties_participants_count INT,
    PRIMARY KEY (accident_id),
    FOREIGN KEY (accident_id) REFERENCES dds.hub_accident (accident_id)
);
