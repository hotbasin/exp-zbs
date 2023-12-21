#!/usr/bin/python3

import json

import requests


''' =====----- Global variables -----===== '''

# IP-адрес/FQDN и порт тестируемого сервера
SRV_ADDR = '127.0.0.1:8080'
# SRV_ADDR = 'zonest.ssszone.ru:7077'


''' =====----- Functions -----===== '''

# Проверка / и /index
def test_index(path_: str='') -> str:
    response_ = requests.get(f'https://{SRV_ADDR}' + path_)
    return response_.text


# Проверка /srv1/auth/login
def test_login_post(credentials: dict) -> str:
    response_ = requests.post(f'http://{SRV_ADDR}/srv1/auth/login',
                              json=credentials)
    return response_.json()


# Проверка /srv2/auth/login
def test_login_get(credentials: dict) -> str:
    response_ = requests.get(f'http://{SRV_ADDR}/srv2/auth/login',
                             params=credentials)
    return response_.json()


# Проверка /random_data
def test_random_get() -> str:
    response_ = requests.get(f'http://{SRV_ADDR}/random_data')
    return response_.text


# Проверка /srv1/model/ini_bin_upload
def test_bin_upload_post(sample_file: str) -> str:
    with open(sample_file, 'rb') as fb_:
        file_ = {'file': ('test_f.csv', fb_)}
        response_ = requests.post(f'http://{SRV_ADDR}/srv1/model/ini_bin_upload',
                                  files=file_)
    return response_.text


'''
def test_txt_upload_post(sample_file: str) -> str:
    with open(sample_file, 'r') as ft_:
        file_ = {'file': ('test_f.csv', ft_)}
        response_ = requests.post(f'http://{SRV_ADDR}/srv1/model/ini_txt_upload',
                                  files=file_)
    return response_.text
'''


''' =====----- MAIN -----===== '''

if __name__ == '__main__':
    #####=====----- Тест / -----=====#####
    print(test_index('/'))

    #####=====----- Тест login -----=====#####
    # creds = {'login': 'user1', 'password': 'qwerty1'}
    # print(test_login_post(creds))
    # print(test_login_get(creds))

    #####=====----- Тест random_data -----=====#####
    # print(test_random_get())

    #####=====----- Тест upload -----=====#####
    # print(test_bin_upload_post('test_file.csv'))
    # print(test_txt_upload_post('test_file.csv'))

#####=====----- THE END -----=====#########################################