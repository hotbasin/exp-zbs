#!/usr/bin/python3

import sys
sys.path.append('VENV\\Lib\\site-packages')

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def server_root() -> str:
    return 'It is works'

#####=====----- THE END -----=====#########################################