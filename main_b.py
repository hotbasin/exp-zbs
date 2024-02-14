#!/usr/bin/python3

''' Code is based on
https://fastapi.tiangolo.com/ru/tutorial/security/first-steps/
'''

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
sys.path.append('VENV/lib/python3.10/site-packages')
sys.path.append('VENV/lib/python3.11/site-packages')
sys.path.append('~/.local/bin')
#################################################

from pathlib import Path
from time import time
from typing import Annotated

from fastapi import FastAPI, responses, File, UploadFile, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import uvicorn

import srv_api_a as api_
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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


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

def fake_decode_token(token):
    return User(username=token+'fakedecoded', email='ss@dd.ru', full_name='Stalk Spectrum')
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


''' =====----- Endpoints -----===== '''

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(e_.ROOT_INDEX_FILE)


@srv.get('/items/')
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {'token': token}
@srv.get('users/me')
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    if Path(e_.ROOT_CERT_FILE).exists() and \
       Path(e_.HOST_CERT_FILE).exists() and \
       Path(e_.PRIV_KEY_FILE).exists():
        uvicorn.run(
            'main_b:srv',
            host=e_.APP_HOST,
            port=e_.APP_PORT,
            reload=True,
            ssl_ca_certs=e_.ROOT_CERT_FILE,
            ssl_certfile=e_.HOST_CERT_FILE,
            ssl_keyfile=e_.PRIV_KEY_FILE
        )
    else:
        uvicorn.run(
            'main_b:srv',
            host=e_.APP_HOST,
            port=e_.APP_PORT,
            reload=True
        )

#####=====----- THE END -----=====#########################################