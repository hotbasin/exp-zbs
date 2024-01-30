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
# Временная база для модели
MODEL_DB_PATH = 'sqlite:///sqlite/model2.sqlite3'
ModelBase = declarative_base()
MODEL_ENGINE = sa.create_engine(MODEL_DB_PATH)
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

class File(Base):
    __tablename__ = 'File'
    id = sa.Column(sa.Integer, primary_key=True)
    filename = sa.Column(sa.String(1024))
    filesize = sa.Column(sa.Integer)
    loaddate = sa.Column(sa.Float)

class Model_Base(ModelBase):
    __tablename__ = 'Students'
    p_key = sa.Column(sa.Integer(), nullable=False, unique=True, primary_key=True, autoincrement=True)
    date = sa.Column(sa.String())
    id = sa.Column(sa.Text())
    utc = sa.Column(sa.String())
    steck = sa.Column(sa.Text())
    spec = sa.Column(sa.Text())
    role = sa.Column(sa.Text())
    role_in = sa.Column(sa.Text())
    hour_per_week = sa.Column(sa.Text())
    other_courses = sa.Column(sa.Text())
    time_of_studies = sa.Column(sa.Text())
    notes = sa.Column(sa.Text())
    language = sa.Column(sa.String())
    in_chat = sa.Column(sa.String())
    out = sa.Column(sa.Text())
    prediction = sa.Column(sa.Float())

##### Base.metadata.create_all(MODEL_ENGINE)


''' =====----- Decorators -----===== '''

def token_decor(fn_to_be_decor):
    def fn_wrapper(**kwargs):
        ok_ = False
        payload_ = dict()
        if 'token' in kwargs.keys():
            token = kwargs['token']
            try:
                with Session(ENGINE) as s_:
                    user_ = s_.query(User).filter(User.acc_token == token).first()
                try:
                    if user_.acc_expired > time():
                        # TTL токена не закончилось
                        ok_ = True
                except:
                    # TTL токена закончилось или его нет
                    ok_ = False
            except:
                # Что-то не так с БД
                ok_ = False
        # result_ = fn_to_be_decor(auth_ok=ok_, payload=payload_, **kwargs)
        result_ = fn_to_be_decor(auth_ok=ok_, **kwargs)
        return result_
    return fn_wrapper


''' =====----- API Methods -----===== '''

def post_login(credentials: dict) -> dict:
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
                    # Обновление пользователя в базе
                    user_.acc_token = str(uuid.uuid4())
                    user_.ref_token = str(uuid.uuid4())
                    user_.acc_expired = time() + ACC_TTL
                    user_.ref_expired = time() + REF_TTL
                    s_.add(user_)
                    s_.commit()
                    # Формирование ответа
                    output_dict_['status'] = 'success'
                    output_dict_['text'] = f'User {user_.login}: logged in'
                    output_dict_['acc_token'] = user_.acc_token
                    output_dict_['acc_expired'] = user_.acc_expired
                    output_dict_['ref_token'] = user_.ref_token
                    output_dict_['ref_expired'] = user_.ref_expired
                else:
                    output_dict_['text'] = f'User {user_.login}: login failed'
            else:
                output_dict_['text'] = f'User {login_}: not exists'
    except Exception as e_:
        print(e_)
    # return json.dumps(output_dict_, ensure_ascii=False, indent=2)
    return output_dict_


def post_refresh_token(refresh_access: dict) -> dict:
    ''' Метод для обновления access-token через действующий
    refresh-token
    Arguments:
        refresh_access [dict] -- Словарь/json с ключом "ref_token"
    Returns:
        [dict] -- Словарь/json с ключами "status", "text", "acc_token",
            "acc_expired" или с ключами "status", "text" в случае ошибки
    '''
    output_dict_ = {'status': 'fail',
                    'text': 'Unknown request'
                   }
    try:
        with Session(ENGINE) as s_:
            ref_token_ = refresh_access['ref_token']
            user_ = s_.query(User).filter(User.ref_token == ref_token_).first()
            if user_:
                if user_.ref_expired > time():
                    # Обновление токена пользователя в базе
                    user_.acc_token = str(uuid.uuid4())
                    user_.acc_expired = time() + ACC_TTL
                    s_.add(user_)
                    s_.commit()
                    # Формирование ответа
                    output_dict_['status'] = 'success'
                    output_dict_['text'] = f'User {user_.login}: new access-token generated'
                    output_dict_['acc_token'] = user_.acc_token
                    output_dict_['acc_expired'] = user_.acc_expired
                else:
                    output_dict_['text'] = 'This refresh-token expired, need login again'
            else:
                output_dict_['text'] = 'No such token'
    except Exception as e_:
        print(e_)
    return output_dict_


def get_random_data():
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


# def get_random_data_t(auth_ok=False, payload=None, **kwargs):
@token_decor
def get_random_data_t(auth_ok=False, **kwargs):
    if auth_ok:
        return get_random_data()
    else:
        output_dict_ = {'status': 'fail',
                        'text': 'Unauthorized request'
                       }
        return output_dict_


def get_datafile() -> dict:
    ''' Выдаёт атрибуты последнего удачно загруженного файла с данными
    Returns:
        [dict] -- словарь/json с ключами 'filename': (str),
            'filesize': (int), 'loaddate': (float)
    '''
    output_dict_ = dict()
    with Session(ENGINE) as s_:
        filedata_ = s_.query(File).first()
    output_dict_['filename'] = filedata_.filename
    output_dict_['filesize'] = filedata_.filesize
    output_dict_['loaddate'] = filedata_.loaddate
    return output_dict_


def update_last_file_data(filename: str, filesize: int, loaddate: float):
    with Session(ENGINE) as s_:
        filedata_ = s_.query(File).first()
        filedata_.filename = filename
        filedata_.filesize = filesize
        filedata_.loaddate = loaddate
        s_.add(filedata_)
        s_.commit()


def get_predictions():
    ''' Выдает список предсказанных вероятностей поимённо
    Returns:
        [json] -- Список словарей
    '''
    output_list_ = []
    with Session(MODEL_ENGINE) as t_:
        all_predictions = t_.query(Model_Base).all()
    for student in all_predictions:
        output_list_.append({'p_key': student.p_key,
                             'tg_id': student.id,
                             'project_role': student.role_in,
                             'prediction': student.prediction
                           })
    return output_list_

#####=====----- THE END -----=====#########################################