#!/usr/bin/python3

import requests

''' =====----- Global variables -----===== '''

# IP-адрес/FQDN и порт тестируемого сервера
SRV_ADDR = 'localhost:8080'


''' =====----- Functions -----===== '''

def test_root() -> str:
    r = requests.get(f'http://{SRV_ADDR}')
    return r.text


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    print(test_root())

#####=====----- THE END -----=====#########################################