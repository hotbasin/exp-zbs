#!/usr/bin/python3

#####=====----- TEMPORAL for VENV -----=====#####
# import sys
# sys.path.append('VENV\\Lib\\site-packages')
#################################################

import json
import uuid
from time import time
from random import choice, random

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Session


''' =====----- Global variables -----====='''

# Настройки для SQLAlchemy
DB_PATH = 'sqlite:///sqlite/users.sqlite3'
Base = declarative_base()
ENGINE = sa.create_engine(DB_PATH)
# Время жизни access-token
ACC_TTL = 600.0
# Время жизни refresh-token
REF_TTL = 3600.0


''' =====----- Classes -----===== '''

class User(Base):
    __tablename__ = 'Users'
    uid = sa.Column(sa.String(36), primary_key=True)
    admin = sa.Column(sa.Boolean)
    name = sa.Column(sa.String(1024))
    login = sa.Column(sa.String(1024))
    password = sa.Column(sa.String(1024))
    acc_token = sa.Column(sa.String(36))
    acc_expired = sa.Column(sa.Float)
    ref_token = sa.Column(sa.String(36))
    ref_expired = sa.Column(sa.Float)
    comment = sa.Column(sa.Text(1024))


''' =====----- API Methods -----===== '''

def login_getpost(credentials: dict) -> dict:
    ''' Метод для аутентификации на сервере. При логине пользователя
    записывает ему в таблицу "Users" выданные access-token и refresh-token
    и время окончания их действия "acc_expired" и "ref_expired".
    Arguments:
        credentials [dict] -- Словарь/json с ключами "login", "password"
    Returns:
        [dict] -- Словарь/json с ключами "status", "text", "acc_token",
            "acc_expired", "ref_token", "ref_expired"
            или с ключами "status", "text" в случае ошибки
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    try:
        with Session(ENGINE) as s_:
            login_ = credentials['login']
            password_ = credentials['password']
            user_ = s_.query(User).filter(User.login == login_).first()
            if user_:
                if user_.password == password_:
                    acc_token_ = str(uuid.uuid4())
                    ref_token_ = str(uuid.uuid4())
                    # Обновление пользователя в базе
                    user_.acc_token = acc_token_
                    user_.ref_token = ref_token_
                    user_.acc_expired = time() + ACC_TTL
                    user_.ref_expired = time() + REF_TTL
                    s_.add(user_)
                    s_.commit()
                    # Формирование ответа
                    output_dict_['status'] = 'success'
                    output_dict_['text'] = f'User {login_}: logged in'
                    output_dict_['acc_token'] = acc_token_
                    output_dict_['acc_expired'] = user_.acc_expired
                    output_dict_['ref_token'] = ref_token_
                    output_dict_['ref_expired'] = user_.ref_expired
                else:
                    output_dict_['text'] = f'User {login_}: login failed'
            else:
                output_dict_['text'] = f'User {login_}: not exists'
    except Exception as e_:
        print(e_)
    # return json.dumps(output_dict_, ensure_ascii=False, indent=2)
    return output_dict_


def random_data_get():
    ''' Для отладки взаимодействия с frontend.
    Отдаёт json (список словарей) со случайными значениями [float] в
    интервале [0, 1] по неким именам.
    Returns:
        [json] -- Список словарей
    '''
    output_list_ = []
    name_list_ = [
        'William', 'Shatner', 'Kirk', 'Leonard', 'Nimoy',
        'Spock', 'DeForest', 'Kelley', 'McCoy', 'James',
        'Doohan', 'Scott', 'Nichelle', 'Nichols', 'Uhura',
        'Walter', 'Koenig', 'Chekov', 'George', 'Takei',
        'Sulu', 'Picard', 'Riker', 'LaForge', 'Yar',
        'Worf', 'Crusher', 'Troi', 'Data', 'Wesley'
        ]
    for i_ in range(0, 3):
        output_list_.append({'name': choice(name_list_), 'prob': round(random(), 2)})
    return output_list_

#####=====----- THE END -----=====#########################################