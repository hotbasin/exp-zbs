#!/usr/bin/python3

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
sys.path.append('VENV/lib/python3.10/site-packages')
sys.path.append('VENV/lib/python3.11/site-packages')
sys.path.append('~/.local/bin')
#################################################

from os import path

from fastapi import FastAPI, responses
import uvicorn

import srv_api as api_

''' =====----- Global variables -----===== '''

# Корневой index.html
ROOT_INDEX_FILE = 'static/index.html'
srv = FastAPI()


''' =====----- Endpoints -----===== '''

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(ROOT_INDEX_FILE)


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    uvicorn.run(
        'main:srv',
        host='0.0.0.0',
        port=7077,
        reload=True,
        ssl_ca_certs='certs/ca_certificate.crt',
        ssl_certfile='certs/certificate.crt',
        ssl_keyfile='certs/private.key'
    )

#####=====----- THE END -----=====#########################################