# Пет-проект по анализу ДТП в Москве

Данный проект основан на анализе ДТП в городе Москва и включает в себя обработку данных расположения камер фото-и видеофиксации (КФВФ), обучение модели машинного обучения для определения степени тяжести увечий при ДТП по входящим признакам, а также проверки гипотезы.

# Описание

Для решения задачи обработки и анализа данных ДТП в Москве, был создан пайплайн с тремя слоями: stg, ods, dds, cdm. Пайплайн выгружает данные из двух источников - камеры КФВФ и информации о ДТП в городе Москва, и будет выполняться 1 раз в месяц с помощью Airflow.

Далее, происходит обучение модели машинного обучения, которая определяет степень тяжести увечий при ДТП по входящим признакам. Эта модель необходима для скорой помощи, чтобы быстрее и точнее определить степень тяжести травм и выделить срочные случаи.

Кроме того, проект включает в себя анализ данных и проверку гипотезы: "На участках автомобильных дорог с непрерывным оптическим/радиолокационным покрытием камерами фото- и видеофиксации регистрируется меньшее число ДТП нежели на участках, где такового покрытия нет".

В конце проекта будет осуществлена визуализация данных с помощью Tableau.

# Навигация по проекту

[Dags Airflow](https://github.com/slava87VS/Project_Moscow_DTP/tree/main/finish/dags)

[Schema star](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/schema_database/shema_star.png)

[DWH SQL](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/sql/create_star.sql)

[Visualization](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/visualization/visualization.md)

[Machine Learning](https://github.com/slava87VS/Project_Moscow_DTP/tree/main/finish/ml)

[Структура данных ДТП](https://github.com/slava87VS/Project_Moscow_DTP/blob/main/finish/struktura_data_DTP.py)


# Установка и запуск

Чтобы запустить проект на своей машине, выполните следующие шаги:

Клонируйте репозиторий к себе на компьютер:
```
git clone https://github.com/your_username/dtp_analysis.git
```
Установите зависимости:
```
pip install -r requirements.txt
```
