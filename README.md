<h3 align="center">:gb: Disclaimer</h3>

:warning: This project is intended for use in a company with Russian-speaking
specialists. Therefore, all explanations, comments, and other texts are provided
in Russian only.

----

# :ru: Проект-полигон для отработки модели &laquo;Воронка HR&raquo; #
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
[2. DONE](#done)    
[3. TODO](#todo)    
[4. Решение](#решение)    
[5. Результат](#результат)    
[6. Запуск проекта](#запуск-проекта)    

## Задание ##

1. Существует отработанная и обученная модель для предсказания вероятности ухода
человека с какого-либо рабочего проекта до его завершения. Требуется создать
backend-часть для приёма данных, обработки и выдачи результатов.
2. Испольщование FastAPI, Uvicorn.
3. Использование SQLite для работы с БД.
4. Последующий переход на PostgreSQL.
5. Применение Docker container
6. Авторизация OAuth2 (по возможности с JWT)

[:arrow_up: Содержание](#содержание)

----

## DONE ##

- Метод POST **`/srv1/auth/login`**
- Метод POST **`/srv1/auth/refresh`**
- Метод GET **`/random_data`**
- Метод GET **`/data-file`**
- Метод GET **`/predictions`**
- Метод POST **`/srv1/model/ini_bin_download`**
- Метод POST **`/srv1/model/data_upload`**
- SSL-сертификат от Let;s Encrypt. Установка `certbot`

----

## TODO ##

- Авторизация OAuth2 [как описано в документации](https://fastapi.tiangolo.com/ru/tutorial/security/first-steps/)
- Метод GET **`/srv1/random_data`** с авторизацией
- Метод GET **`/srv1/data-file`** с авторизацией
- Метод GET **`/srv1/predictions`** с авторизацией
- Переход на PostgreSQL
- Освоение и перехват CI/CD
- Создание &laquo;админки&raquo; для управления пользовательскими учётками

----

## Решение ##

[:arrow_up: Содержание](#содержание)

----

## Результат ##

[:arrow_up: Содержание](#содержание)

----

## Запуск проекта ##

Проект запускается в docker-container на сервере с ОС Ubuntu Server LTS (Jammy).

Каноническая установка docker и docker-compose (под `sudo -i`):

1. Обычное обновление
```bash
apt update
```
2. Проверить наличие пакетов через `apt search`. Обычно они уже есть, но при
отсутствии установить:
```bash
apt install ca-certificates
apt install curl
apt install gnupg
apt install software-properties-common
```
3. Скачать GPG-ключ репозитория Docker:
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
4. Создать `/etc/apt/sources.list.d/docker.list`, в котором:
```text
deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download/docker.com/linux/ubuntu jammy stable
```
5. Ещё раз
```bash
apt update
```
6. Проверить на всякий случай, что установка будет из репозитория Docker:
```bash
apt-cache policy docker-ce
```
7. Собственно установка:
```bash
apt install docker-ce
apt install docker-ce-cli
apt install containerd.io
apt install docker-buildx-plugin
apt install docker-compose-plugin
```
8. Проверка:
```bash
systemctl status docker.service
```
Или ещё можно запустить тестовый контейнер:
```bash
docker run hello-world
```
9. В файле `/etc/group` добавить своего пользователя в группу `docker`.
10. Сборка docker-image:
```bash
cd ${PROJECT_DIR}
docker build -t zbs:ver1 .
```
11. Запуск контейнера
```bash
docker run -d -p 8080:7077/tcp zbs:ver1
```

Для корректной работы обученных моделей рекомендуется установка библиотек
конкретных версий и в следующем порядке (перед формированием итогового файла
`requirements.txt`):

1. numpy==1.23.5
2. pandas==1.5.3
3. scikit-learn==1.2.2
4. category-encoders==2.6.3
5. imbalanced-learn==0.10.1 + imblearn
6. pyxl/openpyxl&nbsp;&mdash; для возможности обработки файлов Excel

Предположительно имеет смысл порядок установки

```bash
pip install "fastapi[all]"
```

Должно быть эквивалентно:

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

[:arrow_up: Содержание](#содержание)

----
