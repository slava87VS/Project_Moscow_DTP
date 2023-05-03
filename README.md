# Навигация по проекту

[Dags Airflow](https://github.com/slava87VS/Project_Moscow_DTP/tree/main/finish/dags)

[Schema star](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/schema_database/shema_star.png)

[DWH SQL](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/sql/create_star.sql)

[Visualization](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/visualization/visualization.md)

[Machine Learning](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/ml/ml.ipynb)

[Hypothesis](https://colab.research.google.com/drive/1cEEkOUOoM7EHtv6q5NZpZy9-7DhlOwJd?usp=sharing)

[Структура данных ДТП](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/struktura_data_DTP.py)

# Пет-проект по анализу ДТП в Москве

Данный проект основан на анализе ДТП в городе Москве и включает в себя: разработку DWH, автоматизацию обработки и выгрузки данных, анализ данных расположения камер фото-и видеофиксации (КФВФ), обучение модели машинного обучения для определения степени тяжести увечий при ДТП по входящим признакам, а также проверки гипотезы и визуализация.

# Описание

Для решения задачи обработки и анализа данных ДТП в Москве, был создан пайплайн с тремя слоями: stg, ods, dds, cdm. Пайплайн выгружает данные из двух источников - камеры КФВФ и информации о ДТП в городе Москва, и будет выполняться 1 раз в месяц с помощью Airflow.

Далее, происходит обучение модели машинного обучения, которая определяет степень тяжести увечий при ДТП по входящим признакам. Эта модель необходима для скорой помощи, чтобы быстрее и точнее определить степень тяжести травм и выделить срочные случаи.

Кроме того, проект включает в себя анализ данных и проверку гипотезы: "На участках автомобильных дорог, оборудованных и знаком ограничения скорости, и знаком о работе камер фото- и видеофиксации, регистрируется меньшее число ДТП, чем на участках автомобильных дорог, оборудованных только знаками ограничения скорости".

В конце проекта будет осуществлена визуализация данных с помощью Tableau.
