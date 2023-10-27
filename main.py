#!/usr/bin/python3

#####=====----- TEMPORAL for WinDev -----=====#####
import sys
sys.path.append('VENV\\Lib\\site-packages')
###################################################

from fastapi import FastAPI, responses


''' =====----- Global variables -----===== '''

# Корневой index.html
ROOT_INDEX_FILE = 'static/index.html'


app = FastAPI()

# async def server_root() -> str:
@app.get('/')
async def server_root() -> str:
    ''' Аналог index.html в ServerRoot для начальной страницы FastAPI
    Returns:
        [str] -- содержимое HTML-файла, заданного в глобальной
            переменной ROOT_INDEX_FILE
    '''
    # with open(ROOT_INDEX_FILE, 'r', encoding='utf-8') as f_:
        # return f_.read()
    # return "Hello World"
    return responses.FileResponse(ROOT_INDEX_FILE)

#####=====----- THE END -----=====#########################################