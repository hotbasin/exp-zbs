#!/usr/bin/python3

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
sys.path.append('VENV/lib/python3.10/site-packages')
sys.path.append('VENV/lib/python3.11/site-packages')
sys.path.append('~/.local/bin')
#################################################

from os import path
from pathlib import Path
from time import time
from typing import Annotated

from fastapi import FastAPI, responses, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import uvicorn

import srv_api_a as api_


''' =====----- Global variables -----===== '''

srv = FastAPI()
srv.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
# Корневой index.html
ROOT_INDEX_FILE = path.join(path.dirname(path.abspath(__file__)),
                            'static/index.html')
TMP_CSV_FILE = 'tests/binary_file.csv'
TMP_ANKETA_FILE = 'ds_model/file_'
# IP или FQDN сервера, на котором работает приложение
HOST = '0.0.0.0'
# TCP-порт, на котором работает прилржение
PORT=7077
# Файлы сертификатов для SSL/TLS
ROOT_CERT_FILE = 'certs/ca_certificate.crt'
HOST_CERT_FILE = 'certs/certificate.crt'
PRIV_CERT_FILE = 'certs/private.key'


''' =====----- Classes -----===== '''

class Credentials(BaseModel):
    login: str
    password: str


class RefreshToken(BaseModel):
    ref_token: str


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


''' =====----- Functions -----===== '''


''' =====----- Endpoints -----===== '''

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(ROOT_INDEX_FILE)


@srv.post('/srv1/auth/login')
async def post_login(credentials: Credentials):
    ''' Аутентификация на сервере
    '''
    return responses.ORJSONResponse(api_.post_login(dict(credentials)))


@srv.post('/srv1/auth/refresh')
async def post_refresh_token(refresh_access: RefreshToken):
    ''' Обновление access-token через refresh-token
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


##### async def get_random_data_t(tk: str):
@srv.get('/srv1/random_data')
async def get_random_data_t(token: Annotated[str, Depends(oauth2_scheme)]):
    ''' Для проверки авторизованного доступа
    '''
    ##### return responses.ORJSONResponse(api_.get_random_data_t(token=tk))
    return {'token': token}


@srv.get('/data-file')
async def get_datafile():
    ''' Выдаёт атрибуты последнего удачно загруженного файла с данными
    Returns:
        [json] -- словарь/json с ключами 'filename', 'filesize', 'loaddate'
    '''
    return responses.ORJSONResponse(api_.get_datafile())


@srv.get('/srv1/data-file')
async def get_datafile_t(tk: str):
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
    return responses.ORJSONResponse(api_.get_predictions_t(token=tk))


@srv.post('/srv1/model/ini_bin_upload')
async def post_bin_upload(file: UploadFile):
    with open(TMP_CSV_FILE, 'wb') as wb_:
        wb_.write(file.file.read())
    filename_ = file.filename
    filesize_ = file.size
    loaddate_ = time()
    api_.update_last_file_data(filename_, filesize_, loaddate_)
    return responses.JSONResponse({'status': 'File accepted',
                                   'filename': filename_,
                                   'filesize': filesize_,
                                   'loaddate': loaddate_})


@srv.post('/srv1/model/data_upload')
async def post_bin_upload(file: UploadFile):
    filename_ = file.filename
    filesize_ = file.size
    loaddate_ = time()
    model_data_file = TMP_ANKETA_FILE + filename_
    with open(model_data_file, 'wb') as wb_:
        wb_.write(file.file.read())
    api_.update_last_file_data(filename_, filesize_, loaddate_)
    api_.model_works(model_data_file)
    return responses.JSONResponse({'status': 'CSV-File accepted',
                                   'filename': filename_,
                                   'filesize': filesize_,
                                   'loaddate': loaddate_})


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    if Path(ROOT_CERT_FILE).exists() and \
       Path(HOST_CERT_FILE).exists() and \
       Path(PRIV_CERT_FILE).exists():
        uvicorn.run(
            'main_b:srv',
            host=HOST,
            port=PORT,
            reload=True,
            ssl_ca_certs=ROOT_CERT_FILE,
            ssl_certfile=HOST_CERT_FILE,
            ssl_keyfile=PRIV_CERT_FILE
        )
    else:
        uvicorn.run(
            'main_b:srv',
            host=HOST,
            port=PORT,
            reload=True
        )

#####=====----- THE END -----=====#########################################