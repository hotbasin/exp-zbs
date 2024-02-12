#!/usr/bin/python3

from os import environ, path


''' =====----- Global variables -----===== '''

# Корневой index.html
ROOT_INDEX_FILE = path.join(path.dirname(path.abspath(__file__)),
                            'static/index.html')
# Файлы сертификатов для SSL/TLS
ROOT_CERT_FILE = 'certs/ca_certificate.crt'
HOST_CERT_FILE = 'certs/certificate.crt'
PRIV_KEY_FILE = 'certs/private.key'
CSV_FILE = 'tests/binary_file.csv'
ANKETA_FILE_PREFIX = 'ds_model/file_'

# Значения по умолчанию для переменных программного окружения приложения
APP_HOST_DEFAULT = '0.0.0.0'
APP_PORT_DEFAULT = '7077'
DB_HOST_DEFAULT = '127.0.0.1'
DB_PORT_DEFAULT = '5432'
DB_USER_DEFAULT = 'user1'
DB_PASS_DEFAULT = 'qwerty1'
DB_NAME_DEFAULT = 'db.zbs'


''' =====----- Импорт/задание переменных окружения -----===== '''

if app_host_ := environ.get('APP_HOST'):
    APP_HOST = app_host_
else:
    APP_HOST = APP_HOST_DEFAULT


if app_port_ := environ.get('APP_PORT'):
    APP_PORT = int(app_port_)
else:
    APP_PORT = int(APP_PORT_DEFAULT)


if db_host_ := environ.get('DB_HOST'):
    DB_HOST = db_host_
else:
    DB_HOST = DB_HOST_DEFAULT


if db_port_ := environ.get('DB_PORT'):
    DB_PORT = int(db_port_)
else:
    DB_PORT = int(DB_PORT_DEFAULT)


if db_user_ := environ.get('DB_USER'):
    DB_USER = db_user_
else:
    DB_USER = DB_USER_DEFAULT


if db_pass_ := environ.get('DB_PASS'):
    DB_PASS = db_pass_
else:
    DB_PASS = DB_PASS_DEFAULT


if db_name_ := environ.get('DB_NAME'):
    DB_NAME = db_name_
else:
    DB_NAME = DB_NAME_DEFAULT

#####=====----- THE END -----=====#########################################