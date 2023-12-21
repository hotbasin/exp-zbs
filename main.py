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


''' =====----- Global variables -----===== '''

# Корневой index.html
ROOT_INDEX_FILE = 'static/index.html'
app = FastAPI()


''' =====----- Endpoints -----===== '''

@app.get('/')
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
        'main:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
        ssl_ca_certs='certs\WF_certificate_ca.crt',
        ssl_certfile='certs\WF_certificate_x509.crt',
        ssl_keyfile='certs\WF_private.key'
    )

#####=====----- THE END -----=====#########################################