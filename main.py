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
    import os
    os.system('uvicorn main:app --reload')

#####=====----- THE END -----=====#########################################