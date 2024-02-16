#!/usr/bin/python3

''' Code is based on
https://fastapi.tiangolo.com/ru/tutorial/security/first-steps/

!!! This is non-Annotated version !!!
'''

#####=====----- TEMPORAL for VENV -----=====#####
import sys
sys.path.append('VENV/Lib/site-packages')
# sys.path.append('VENV/lib/python3.10/site-packages')
# sys.path.append('VENV/lib/python3.11/site-packages')
# sys.path.append('~/.local/bin')
#################################################

from pathlib import Path
# from time import time
from typing import Annotated

from fastapi import (FastAPI, Depends, HTTPException, status)
##### from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn

##### import srv_api_a as api_
import set_env as e_

fake_users_db = {
    "john": {
        "username": "john",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "secret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "secret2",
        "disabled": True,
    },
}

srv = FastAPI()

def fake_hash_password(password: str):
    # return 'fakehashed' + password
    return password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str=Depends(oauth2_scheme)):
    print(f'TOKEN={str(token)}')    #####<<<<< undefined
    user = fake_decode_token(token)
    # user = fake_decode_token('john')
    print(f'USER={str(user)}')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid credentials in _{str(user)}_',     #####<<<<< None
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user

async def get_current_active_user(current_user: User=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user

@srv.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    return responses.FileResponse(e_.ROOT_INDEX_FILE)

# @srv.get('/items/')
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {'token': token}

@srv.post('/token')
async def login(form_data: OAuth2PasswordRequestForm=Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect user or passwd')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail='Incorrect user or passwd')
    return {'acc_token': user.username, 'token_type': 'bearer'}

@srv.get('/users/me')
async def read_users_me(current_user: User=Depends(get_current_active_user)):
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