#!/usr/bin/python3

import json
from time import ctime

import requests


''' =====----- Global variables -----===== '''

# Временный файл для хранения access-токена
TOKEN_FILE = 'acc-token.json'
# IP-адрес/FQDN и порт тестируемого сервера
SRV_ADDR = '127.0.0.1:7077'
# SRV_ADDR = 'zonest.ssszone.ru:7077'


''' =====----- Functions -----===== '''

# Проверка / и /index
def test_index(path_: str='') -> str:
    response_ = requests.get(f'http://{SRV_ADDR}' + path_)
    return response_.text


# Проверка /srv1/auth/login
def test_login_post(credentials: dict) -> str:
    ''' Тест аутентификации на ресурсе сервера.
    Делает POST-запрос на сервер, login и password вкладывает в json.
    При удачном ответе в json {status: "success"} записывает полученный
    access-токен и его время окончания действия (в читаемом формате) во
    временный файл, указанный в глобальной переменной TOKEN_FILE для
    использования в других тестах.
    Arguments:
        credentials [dict] -- Логин и пароль
    Returns:
        [str] -- Отформатированный многострочник со значениями
            text/acc_token/expired в случае успеха
            или со значением 'text' при ошибке
    '''
    response_ = requests.post(f'http://{SRV_ADDR}/srv1/auth/login',
                              json=credentials)
    ##### return response_.json()
    response_dict = response_.json()
    if response_dict['status'] == 'success':
        text_ = response_dict['text']
        acc_token_ = response_dict['acc_token']
        acc_expired_ = response_dict['acc_expired']
        ref_token_ = response_dict['ref_token']
        ref_expired_ = response_dict['ref_expired']
        token_dict = {'acc_token': acc_token_,
                      'acc_expired': ctime(acc_expired_),
                      'ref_token': ref_token_,
                      'ref_expired': ctime(ref_expired_)
                     }
        with open(TOKEN_FILE, 'w', encoding='utf-8') as t_:
            json.dump(token_dict, t_, ensure_ascii=False, indent=4)
        ret_str = f'Result: {text_}\n' + \
                  f'Access-token: {acc_token_}\n' + \
                  f'Expired: {ctime(acc_expired_)}\n' + \
                  f'Refresh-token: {ref_token_}\n' + \
                  f'Expired: {ref_expired_}'
        return ret_str
    else:
        # return f"FAIL: {response_dict['text']}"
        return response_.json()


# Проверка /srv2/auth/login
def test_login_get(credentials: dict) -> str:
    response_ = requests.get(f'http://{SRV_ADDR}/srv1/auth/login',
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
    # print(test_index('/'))

    #####=====----- Тест login -----=====#####
    creds = {'login': 'user1', 'password': 'qwerty1'}
    print(test_login_post(creds))
    # print(test_login_get(creds))

    #####=====----- Тест random_data -----=====#####
    # print(test_random_get())

    #####=====----- Тест upload -----=====#####
    # print(test_bin_upload_post('test_file.csv'))
    # print(test_txt_upload_post('test_file.csv'))

#####=====----- THE END -----=====#########################################