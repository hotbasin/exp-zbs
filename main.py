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

from fastapi import FastAPI, responses, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

import srv_api as api_


''' =====----- Global variables -----===== '''

srv = FastAPI()
srv.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
# Корневой index.html
ROOT_INDEX_FILE = path.join(path.dirname(path.abspath(__file__)),
                            'static/index.html')
TMP_CSV_FILE = 'tests/binary_file.csv'
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


''' =====----- Endpoints -----===== '''

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(ROOT_INDEX_FILE)


@srv.get('/random_data')
async def get_random_data() -> str:
    ''' Для отладки взаимодействия с frontend.
    Отдаёт json (список словарей) со случайными значениями [float] в
    интервале [0, 1] по неким именам.
    Returns:
        [json] -- Список словарей
    '''
    return responses.ORJSONResponse(api_.get_random_data())


@srv.get('/data-file')
async def get_datafile():
    ''' Выдаёт атрибуты последнего удачно загруженного файла с данными
    Returns:
        [json] -- словарь/json с ключами 'filename', 'filesize', 'loaddate'
    '''
    return responses.ORJSONResponse(api_.get_datafile())


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


@srv.get('/predictions')
async def get_predictions() -> str:
    ''' Выдает список предсказанных вероятностей поимённо
    Returns:
        [json] -- Список словарей
    '''
    return responses.ORJSONResponse(api_.get_predictions())


@srv.post('/srv1/auth/login')
async def post_login(credentials: Credentials):
    ''' Аутентификация на сервере
    '''
    return responses.ORJSONResponse(api_.post_login(dict(credentials)))


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    if Path(ROOT_CERT_FILE).exists() and \
       Path(HOST_CERT_FILE).exists() and \
       Path(PRIV_CERT_FILE).exists():
        uvicorn.run(
            'main:srv',
            host=HOST,
            port=PORT,
            reload=True,
            ssl_ca_certs=ROOT_CERT_FILE,
            ssl_certfile=HOST_CERT_FILE,
            ssl_keyfile=PRIV_CERT_FILE
        )
    else:
        uvicorn.run(
            'main:srv',
            host=HOST,
            port=PORT,
            reload=True
        )

#####=====----- THE END -----=====#########################################