#!/usr/bin/python3

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
sys.path.append('VENV/lib/python3.10/site-packages')
sys.path.append('VENV/lib/python3.11/site-packages')
sys.path.append('~/.local/bin')
#################################################

from os import path
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
async def random_data_get() -> str:
    ''' Для отладки взаимодействия с frontend.
    Отдаёт json (список словарей) со случайными значениями [float] в
    интервале [0, 1] по неким именам.
    Returns:
        [json] -- Список словарей
    '''
    return responses.ORJSONResponse(api_.random_data_get())


@srv.post('/srv1/auth/login')
async def login_post(credentials: Credentials):
    ''' Аутентификация на сервере
    '''
    return responses.ORJSONResponse(api_.login_getpost(dict(credentials)))


@srv.post('/srv1/model/ini_bin_upload')
async def bin_upload_post(file: UploadFile):
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


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    uvicorn.run(
        'main:srv',
        host='0.0.0.0',
        port=7077,
        reload=True,
        # ssl_ca_certs='certs/ca_certificate.crt',
        # ssl_certfile='certs/certificate.crt',
        # ssl_keyfile='certs/private.key'
    )

#####=====----- THE END -----=====#########################################