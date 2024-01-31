# Проект-полигон для отработки модели &laquo;Воронка HR&raquo; #
Backend, DE, DA, ML experiment

![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=plastic&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=plastic&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=plastic&logo=Matplotlib&logoColor=black)
![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=plastic&logo=scipy&logoColor=%white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=plastic&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=plastic&logo=sqlite&logoColor=white)
**`JSON`**
**`FastAPI`**

----

## Содержание ##

[1. Задание](#задание)    
[2. TODO](#todo)    
[3. DONE](#done)    
[4. Решение](#решение)    
[5. Результат](#результат)    
[6. Запуск проекта](#запуск-проекта)    

## Задание ##

1. Испольщование на back-end FastAPI, Uvicorn.
2. Использование SQLite для работы с БД.
3. Последующий переход на PostgreSQL.
4. Применение Docker container

[:arrow_up: Содержание](#содержание)

----

## TODO ##

- Метод GET **`/data-file`**
- Метод GET **`/predictions`**
- Метод POST **`/data-file`**
- Восстановление работы
- Восстановление доступа
- Проверка восстановления

----

## DONE ##

- Метод GET **`/random_data`
- Метод POST **`/srv1/auth/login`**`
- Метод POST **`/srv1/model/ini_bin_download`
- SSL-сертификат от Let;s Encrypt. Установка `certbot`

----

## Решение ##

Для корректной работы обученных моделей рекомендуется установка библиотек
конкретных версий и в следующем порядке:

1. numpy==1.23.5
2. pandas==1.5.3
3. scikit-learn==1.2.2
4. category-encoders==2.6.3
5. imbalanced-learn==0.10.1 + imblearn
6. pyxl/openpyxl&nbsp;&mdash; для возможности обработки файлов Excel

[:arrow_up: Содержание](#содержание)

----

## Результат ##

[:arrow_up: Содержание](#содержание)

----

## Запуск проекта ##

[:arrow_up: Содержание](#содержание)

----
