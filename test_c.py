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
        print(f'get_user() отработала')    #####<<<<<
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    print(f'fake_decode_token() отработала')     #####<<<<<
    return user


def get_current_user(token: str=Depends(oauth2_scheme)):
    print(f'get_current_user() начинает')    #####<<<<<
    print(f'TOKEN={str(token)}')    #####<<<<< undefined
    # user = fake_decode_token(token)
    user = fake_decode_token('john')
    print(f'USER={str(user)}')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid credentials in _{str(user)}_',     #####<<<<< None
            headers={'WWW-Authenticate': 'Bearer'}
        )
    print('get_current_user() отработала')      #####<<<<<
    return user


def get_current_active_user(current_user: User=Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    print('get_current_active_user() отработала')   #####<<<<<
    return current_user


def login(form_data: OAuth2PasswordRequestForm=Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail='Incorrect user or passwd')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail='Incorrect user or passwd')
    return {'acc_token': user.username, 'token_type': 'bearer'}


def read_users_me(current_user: User=Depends(get_current_active_user)):
    print(f'BEGIN={str(current_user)}')
    return current_user


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    print(read_users_me())

#####=====----- THE END -----=====#########################################