А вот тут лучше указать более подробное описание скриптов, потому-что пока всё что я знаю про них из ридмишки, это что они "Dags Airflow". Далее я могу лишь предполагать что есьт что...

Итак, что можно сделать по пунктам:

- [cdm](#cdm)  
- [dds](#dds)  
- [ods](#ods)
- [stg_DTP](#stg_DTP) 
- [stg_milestones](#stg_milestones) 


# [cdm.py](cdm.py)
<a id="cdm"></a>

1. **Вынеcти конфигурационные параметры в отдельные переменные** - это поможет сделать код более читаемым и удобным для настройки. Также, это позволит легко изменять параметры без изменения кода. Тем более у тебя эта история дальше дублируется в dds.

```py
# Конфигурационные параметры
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'b74c3e6'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB = 'postgres'

# ...

def create_data_mart():
    engine = create_engine(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
    # ...
```

2. **Использовать параметризацию схемы и таблицы** - похоже на предыдущий пункт, это также позволит более гибко управлять именами схемы и таблицы, а также избежать возможных конфликтов существующих таблиц.

```py
# Конфигурационные параметры
SCHEMA_NAME = 'cdm'
TABLE_NAME = 'data_mart'

# ...

def create_data_mart():
    # ...
    data_mart.to_sql(TABLE_NAME, engine, schema=SCHEMA_NAME, if_exists='replace', index=False, method='multi')
    # ...
```

3. **Использовать контекстный менеджер для работы с базой данных** - это позволит гарантировать, что соединение с базой данных будет правильно закрыто после выполнения операций.

```py
# ...
def create_data_mart():
    # ...
    with engine.begin() as connection:
        data_mart.to_sql(TABLE_NAME, connection, schema=SCHEMA_NAME, if_exists='replace', index=False, method='multi')
    # ...
```

4. **Добавить логирование** - это поможет отслеживать прогресс выполнения и обнаруживать возможные проблемы

```py
import logging

# ...
def create_data_mart():
    logging.info('Запуск процесса создания data mart')
    # ...
    logging.info('Завершение процесса создания data mart')
```

5. **Вынести SQL скрипт в отдельный файл** - как всегда советую вынести скрипт в каталог sql и вызывать его оттуда

```py
def create_data_mart():
    engine = get_database_engine()
    with open('sql/create_data_mart.sql', 'r') as f:
        query = f.read()
    data_mart = pd.read_sql_query(query, con=engine)
    data_mart.to_sql('data_mart', engine, schema='cdm', if_exists='replace', index=False, method='multi')
    engine.dispose()
```

# [dds.py](dds.py)
<a id="dds"></a>

1. **Реализовать подключение к базе через вынесенный конфиг** - см. 1 пункт в cdm

2. **Использовать пул соединений для повышения производительности** - Вместо создания нового подключения к базе данных для каждого выполнения запроса используйте пул соединений, чтобы переиспользовать соединения между задачами.

```py
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

engine = create_engine(conn_str, poolclass=NullPool)
```

3. **Вынести полотно кода!** - даг место где ты описываешь что как и почему работает, вставлять сюда 40 строк чистого sql это плохая идея )

4. **Разбить выполнение запросов на отдельные задачи** - Вместо одной большой задачи, содержащей все запросы, разделите их на несколько меньших задач. Это упростит отладку, повысит гибкость и позволит повторно использовать код. 

```py
def truncate_dim_table():
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE dds_1.moskow_dtp_dim CASCADE;")

truncate_dim_table_task = PythonOperator(
    task_id='truncate_dim_table',
    python_callable=truncate_dim_table,
    dag=dag
)

def insert_dim_table():
    with engine.connect() as conn:
        conn.execute("""
...
        """)

insert_dim_table_task = PythonOperator(
    task_id='insert_dim_table',
    python_callable=insert_dim_table,
    dag=dag
)

# Аналогично раздели выполнение запросов для фактов

def truncate_fact_table():
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE dds_1.moskow_dtp_fact CASCADE;")

truncate_fact_table_task = PythonOperator(
    task_id='truncate_fact_table',
    python_callable=truncate_fact_table,
    dag=dag
)

def insert_fact_table():
    with engine.connect() as conn:
        conn.execute("""
...
        """)

insert_fact_table_task = PythonOperator(
    task_id='insert_fact_table',
    python_callable=insert_fact_table,
    dag=dag
)
```

# [ods.py](ods.py)
<a id="ods"></a>

1. **Избегать повторений кода для создания подключения к БД** - `engine = create_engine` повторяется 3 раза, ну не круто

```py
# создание объекта подключения к БД
engine = create_engine(conn_str)
```

2. **Реализовать подключение к базе через вынесенный конфиг** - ого и тут они повторяются см. 1 пункт в cdm

3. **Упростить преобразование данных JSON и улучшить читаемость кода** - если честно не уверен, что это работает, но можно попробовать, видел где-то такую реализацию

```py
# Преобразование данных JSON
def extract_json_value(json_str, *keys):
    data = json.loads(json_str)
    for key in keys:
        data = data.get(key)
        if data is None:
            return None
    return data

accident_df['year'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'year')
accident_df['brand'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'brand')
accident_df['color'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'color')
accident_df['model'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'model')
accident_df['category'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'category')
accident_df['role'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'participants', '0', 'role')
accident_df['gender'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'participants', '0', 'gender')
accident_df['health_status'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'participants', '0', 'health_status')
accident_df['years_of_driving_experience'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'participants', '0', 'years_of_driving_experience')
accident_df['violations'] = accident_df['properties_vehicles'].apply(extract_json_value, '0', 'participants', '0', 'violations')
```

# [stg_DTP.py](stg_DTP.py)
<a id="stg_DTP"></a>

1. **Использовать конфигурационный файл** - тут ещё одно вынесение заметил, создай отдельный файл для хранения конфигурационных параметров, таких как URL, данные аутентификации и т.д. Это позволит легко настраивать приложение и изменять значения без изменения кода.

```py
# config.py

DATABASE_URL = 'postgresql://postgres:b74c3e6@localhost:5432/postgres'
DATA_URL = 'https://cms.dtp-stat.ru/media/opendata/moskva.geojson'

# В коде
import config

def load_data_to_postgres():
    url = config.DATA_URL
    engine = create_engine(config.DATABASE_URL)
    # Остальной код
```

2. **Используй параметры вставки для Pandas** - вместо явного переименования столбцов в DataFrame можно использовать параметр `columns` при вызове `pd.json_normalize`, чтобы привести столбцы к требуемому формату

```py
def load_data_to_postgres():
    # Остальной код
    df = pd.json_normalize(data['features'], 
                           sep='_', 
                           record_path=['properties'],
                           meta=['type', ['geometry', 'type'], ['geometry', 'coordinates']],
                           errors='ignore',
                           meta_prefix='properties_')
    # Остальной код
```

# [stg_milestones.py](stg_milestones.py)
<a id="stg_milestones"></a>

1. **Использовать относительные пути вместо абсолютных путей к файлам** - у меня мак и нет диска C, как я должен считать csv-шку?

```py
milestones = pd.read_csv('data/milestones.csv', sep=';')
```

2. **Разделить код на функции более мелкого размера для повышения читаемости и повторного использования** - тут я думаю и так понятно, в целях масштабирования

```py
def read_csv_file(file_path):
    return pd.read_csv(file_path, sep=';')

def connect_to_database():
    engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
    return engine

def save_to_database(data, engine):
    data.to_sql('milestones', engine, schema='stg', if_exists='replace', index=False, method='multi')
    engine.dispose()

def load_milestones():
    file_path = 'data/milestones.csv'
    milestones = read_csv_file(file_path)
    engine = connect_to_database()
    save_to_database(milestones, engine)
```

ну и соответственно обрабатывать исключения:

```py
import os

def read_csv_file(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, sep=';')
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

def connect_to_database():
    try:
        engine = create_engine('postgresql://postgres:b74c3e6@localhost:5432/postgres')
        return engine
    except Exception as e:
        raise ConnectionError("Failed to connect to the database") from e

def load_milestones():
    file_path = 'data/milestones.csv'
    
    try:
        milestones = read_csv_file(file_path)
        engine = connect_to_database()
        save_to_database(milestones, engine)
    except (FileNotFoundError, ConnectionError) as e:
        # Обработка ошибок или логирование
        print(f"Error occurred: {str(e)}")
```