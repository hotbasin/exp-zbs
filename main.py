#!/usr/bin/python3

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
sys.path.append('VENV/lib/python3.10/site-packages')
sys.path.append('VENV/lib/python3.11/site-packages')
sys.path.append('~/.local/bin')
#################################################

from pathlib import Path
from time import time

from fastapi import FastAPI, responses, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import srv_api as api_
import set_env as e_


''' =====----- Global variables -----===== '''

srv = FastAPI()
srv.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


''' =====----- Classes -----===== '''

class Credentials(BaseModel):
    ''' Класс используется в методе /srv1/auth/login
    '''
    login: str
    password: str


class RefreshToken(BaseModel):
    ''' Класс используется в методе /srv1/auth/refresh
    '''
    ref_token: str


''' =====----- Endpoints -----===== '''

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(e_.ROOT_INDEX_FILE)


@srv.post('/srv1/auth/login')
async def post_login(credentials: Credentials):
    ''' Аутентификация на сервере
    Returns:
        [json] -- json с ключами "status", "text", "acc_token",
            "acc_expired", "ref_token", "ref_expired"
            или с ключами "status", "text" в случае ошибки
    '''
    return responses.ORJSONResponse(api_.post_login(dict(credentials)))


@srv.post('/srv1/auth/refresh')
async def post_refresh_token(refresh_access: RefreshToken):
    ''' Обновление access-token через refresh-token
    Returns:
        [json] -- json с ключами "status", "text", "acc_token",
            "acc_expired" или с ключами "status", "text" в случае ошибки
    '''
    return responses.ORJSONResponse(api_.post_refresh_token(dict(refresh_access)))


@srv.get('/random_data')
async def get_random_data() -> str:
    ''' Для отладки взаимодействия с frontend.
    Отдаёт json (список словарей) со случайными значениями [float] в
    интервале [0, 1] по неким именам.
    Returns:
        [json] -- Список словарей
    '''
    return responses.ORJSONResponse(api_.get_random_data())


@srv.get('/srv1/random_data')
async def get_random_data_t(tk: str):
    ''' Функционал, аналогичный /random_data плюс авторизация
    '''
    return responses.ORJSONResponse(api_.get_random_data_t(token=tk))


@srv.get('/data-file')
async def get_datafile():
    ''' Выдаёт атрибуты последнего удачно загруженного файла с данными
    Returns:
        [json] -- json с ключами 'filename', 'filesize', 'loaddate'
    '''
    return responses.ORJSONResponse(api_.get_datafile())


@srv.get('/srv1/data-file')
async def get_datafile_t(tk: str):
    ''' Функционал, аналогичный /data-file плюс авторизация
    '''
    return responses.ORJSONResponse(api_.get_datafile_t(token=tk))


@srv.get('/predictions')
async def get_predictions() -> str:
    ''' Выдает список предсказанных вероятностей поимённо
    Returns:
        [json] -- Список словарей
    '''
    return responses.ORJSONResponse(api_.get_predictions())


@srv.get('/srv1/predictions')
async def get_predictions_t(tk: str):
    ''' Функционал, аналогичный /predictions плюс авторизация
    '''
    return responses.ORJSONResponse(api_.get_predictions_t(token=tk))


##### @srv.post('/srv1/model/ini_bin_upload')
##### Временная рокировка эндпоинтов
@srv.post('/srv1/model/data_upload')
async def post_bin_upload(file: UploadFile):
    ''' Загружает любой файл Обновляет данные о загруженном файле в БД в
    таблице File.
    '''
    with open(e_.CSV_FILE, 'wb') as wb_:
        wb_.write(file.file.read())
    filename_ = file.filename
    filesize_ = file.size
    loaddate_ = time()
    api_.update_last_file_data(filename_, filesize_, loaddate_)
    return responses.JSONResponse({'status': 'File accepted',
                                   'filename': filename_,
                                   'filesize': filesize_,
                                   'loaddate': loaddate_})


##### @srv.post('/srv1/model/data_upload')
##### Временная рокировка эндпоинтов
@srv.post('/srv1/model/ini_bin_upload')
async def post_model_upload(file: UploadFile):
    ''' Загружает либо готовый файл CSV, либо исходный XLSX, запускает
    обученную модель. Обновляет данные о загруженном файле в БД в
    таблице File. Полученные результаты предсказаний добавлябтся в БД в
    таблицу Students.
    '''
    filename_ = file.filename
    filesize_ = file.size
    loaddate_ = time()
    model_data_file = e_.ANKETA_FILE_PREFIX + filename_
    with open(model_data_file, 'wb') as wb_:
        wb_.write(file.file.read())
    api_.update_last_file_data(filename_, filesize_, loaddate_)
    api_.use_model(model_data_file)
    return responses.JSONResponse({'status': 'CSV-File accepted',
                                   'filename': filename_,
                                   'filesize': filesize_,
                                   'loaddate': loaddate_})


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    if Path(e_.ROOT_CERT_FILE).exists() and \
       Path(e_.HOST_CERT_FILE).exists() and \
       Path(e_.PRIV_KEY_FILE).exists():
        uvicorn.run(
            'main:srv',
            host=e_.APP_HOST,
            port=e_.APP_PORT,
            reload=True,
            ssl_ca_certs=e_.ROOT_CERT_FILE,
            ssl_certfile=e_.HOST_CERT_FILE,
            ssl_keyfile=e_.PRIV_KEY_FILE
        )
    else:
        uvicorn.run(
            'main:srv',
            host=e_.APP_HOST,
            port=e_.APP_PORT,
            reload=True
        )

#####=====----- THE END -----=====#########################################