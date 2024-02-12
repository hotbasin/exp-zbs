#!/usr/bin/python3

from os import environ


''' =====----- Global variables -----===== '''

# Значения по умолчанию для переменных программного окружения приложения
APP_PORT_DEFAULT = '7077'
DB_HOST_DEFAULT = '127.0.0.1'
DB_PORT_DEFAULT = '5432'
DB_USER_DEFAULT = 'user1'
DB_PASS_DEFAULT = 'qwerty1'
DB_NAME_DEFAULT = 'db.zbs'

if app_port_ := environ.get('APP_PORT'):
    APP_PORT = int(app_port_)
else:
    APP_PORT = int(APP_PORT_DEFAULT)

#####=====----- THE END -----=====#########################################