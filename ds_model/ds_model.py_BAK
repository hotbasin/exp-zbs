#!/usr/bin/python3

import pickle
import string

import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import category_encoders as ce
from imblearn.over_sampling import SMOTE


''' =====----- Основная функция предсказаний -----===== '''

def prediction(dataframe: object) -> object:
    ''' Основная функция для выдачи предсказаний
    Arguments:
        dataframe [object] -- Датафрейм, полученный из файла анкеты в формате
            CSV или XLSX
    Returns:
        [object] -- Датафрейм, дополненный признаком fin_pred (вероятность
            выхода)
    '''
    data = dataframe
    # Удаление неинформативных признаков
    data = data.drop(['in_chat'], axis=1)

    ''' Работа с датой и временем '''

    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    data['day_name'] = data['date'].dt.day_name()
    data['day_num'] = data['date'].dt.day_of_week
    data['hour_of_day'] = data['date'].dt.hour
    to_fill = {
        'day_name': 'Friday',
        'day_num': data['day_num'].median(),
        'hour_of_day': data['hour_of_day'].median()
        }
    data = data.fillna(to_fill)

    def get_period(x):
        if 0 < x < 11:
            return 'morning'
        elif 11 < x < 17:
            return 'day'
        elif 17 < x < 23:
            return 'evening'
        else:
            return 'night'

    data['period_of_day'] = data['hour_of_day'].apply(get_period)

    ''' Языки программирования '''

    # Заполнение пропусков
    data['language'].fillna('нуль')

    def get_java(x):
        ''' Разделение Java и JavaScript
        '''
        if str(x).lower() == 'js':
            return 'java'
        else:
            return str(x).lower()    

    data['language'] = data['language'].apply(get_java)
    languages = ['python',
                 'js',
                 'java',
                 'c#',
                 'golang',
                 'php',
                 'c++',
                 'flutter',
                 'qa',
                 'sql'
                ]
    # Бинарное кодирование ЯП
    for lang in languages:
        data[lang] = data['language'].apply(lambda x: 1 if lang in str(x).lower() else 0)

    ''' Роли '''

    def get_role(x):
        ''' Краткое определение предполагаемых ролей и ролей в проекте
        '''
        if 'backend' in str(x).lower() \
                     or 'back' in str(x).lower() \
                     or 'бэк' in str(x).lower():
            return 'backend'
        elif 'frontend' in str(x).lower() \
                        or 'front' in str(x).lower() \
                        or 'фронт' in str(x).lower():
            return 'frontend'
        elif 'аналит' in str(x).lower() \
                      or 'analys' in str(x).lower() \
                      or 'ba' in str(x).lower():
            return 'аналитик'
        elif 'ds' in str(x).lower() \
                  or 'scient' in str(x).lower():
            return 'data scientist'
        elif 'дизайн' in str(x).lower() \
                      or 'design' in str(x).lower() \
                      or 'UX' in str(x).lower():
            return 'дизайнер'
        elif 'project' in str(x).lower() \
                       or 'проект' in str(x).lower():
            return 'project manager'
        elif 'android' in str(x).lower():
            return 'android'
        elif 'ios' in str(x).lower():
            return 'ios'
        elif 'full' in str(x).lower() \
                    or 'develop' in str(x).lower() \
                    or 'разраб' in str(x).lower() \
                    or 'программ' in str(x).lower():
            return 'fullstack'
        elif 'админ' in str(x).lower():
            return 'системный администратор'
        elif 'dev' in str(x).lower():
            return 'devops'
        elif 'qa' in str(x).lower() \
                  or 'тест' in str(x).lower() \
                  or 'test' in str(x).lower():
            return 'тестировщик'
        else:
            return 'other'

    data['role_in_new'] = data['role_in'].apply(get_role)
    data['test_role'] = data['role'].apply(get_role)

    def to_compar(row):
        ''' Бинарное сравнение предполагаемых ролей и ролей в проекте
        '''
        if str(row['test_role']).lower() == str(row['role_in_new']).lower():
            return 1
        else:
            return 0

    data['compar_role'] = data.apply(to_compar, axis=1)

    ''' Время на практику '''

    def get_time(x):
        ''' Кодирование категорий
        '''
        if '10+ часов' in x:
            return 0
        if '20+ часов' in x:
            return 1
        if 'готов работать 25/8' in x:
            return 2

    data['time_par_week'] = data['hour_per_week'].apply(get_time)

    ''' Работа с признаками steck и spec '''

    data['steck'] = data['steck'].fillna('unknown')
    data['spec'] = data['spec'].fillna('unknown')

    def text_clear(text):
        ''' Очистка текста
        '''
        for p in string.punctuation + '\n':
            if p in text:
                text = text.replace(p, '')
        return text

    data['steck'] = data['steck'].apply(text_clear)
    data['spec'] = data['spec'].apply(text_clear)

    data['steck'] = data['steck'].apply(lambda x: x.split())
    data['spec'] = data['spec'].apply(lambda x: x.split())

    def length(iterrows):
        ''' Кодирование категорий
        '''
        for row in iterrows:
            if 1 < len(row) <=2:
                return 1
            if 3 < len(row) <=4:
                return 2
            if 5 < len(row) <=7:
                return 3
            if len(row) > 7:
                return 4
            else:
                return 0

    data['steck_count'] = data['steck'].apply(length)
    data['spec'] = data['spec'].apply(length)
    data['steck_count'] = data['steck_count'].fillna(0)

    ''' Окончательные чистка и кодирование '''

    data = pd.get_dummies(data, columns=['day_name', 'period_of_day'])

    bin_encoder = ce.BinaryEncoder(cols=['role', 'role_in'])
    bin = bin_encoder.fit_transform(data[['role', 'role_in']])
    data = pd.concat([data, bin], axis=1)

    data = data.drop(['hour_of_day', 'qa', 'role_in', 'notes', 'date'], axis=1)

    object_columns = [s for s in data.columns if data[s].dtypes == 'object']
    data.drop(object_columns, axis = 1, inplace=True)

    # Отследить путь к файлу
    with open('ds_model/scaler.pkl', 'rb') as pkl_file:
        scaler = pickle.load(pkl_file)

    # Отследить путь к файлу
    with open('ds_model/model_lr.pkl', 'rb') as pkl_file:
        model_lr = pickle.load(pkl_file)

    # Отследить путь к файлу
    with open('ds_model/model_rf.pkl', 'rb') as pkl_file:
        model_rf = pickle.load(pkl_file)

    threshold_lr_rf = 0.45

    data_s = scaler.transform(data)

    y_lr_pred = pd.Series(model_lr.predict_proba(data_s)[:, 1])
    y_lr_class = y_lr_pred.apply(lambda x: 1 if x > threshold_lr_rf else 0)

    y_rf_pred = pd.Series(model_rf.predict_proba(data)[:, 1])
    y_rf_class = y_rf_pred.apply(lambda x: 1 if x > threshold_lr_rf else 0)

    test = pd.DataFrame({
        'rf_pred': list(y_rf_pred),
        'rf_class': y_rf_class,
        'lr_pred': list(y_lr_pred),
        'lr_class': y_lr_class
        })

    # Отследить путь к файлу
    with open('ds_model/model_dt.pkl', 'rb') as pkl_file:
        model_dt = pickle.load(pkl_file)

    y_dt_pred = pd.Series(model_dt.predict_proba(test)[:, 1])
    df = pd.concat([dataframe, y_dt_pred], axis=1)
    df.columns = ['date',
                  'id',
                  'utc',
                  'steck',
                  'spec',
                  'role',
                  'role_in',
                  'hour_per_week',
                  'other_courses',
                  'time_of_studies',
                  'notes',
                  'language',
                  'in_chat',
                  'fin_pred'
                 ]
    return df


''' EXPERIMENTAL '''
# ini_df = pd.read_csv('ds_model/file_anketa_new.csv', sep='^')
# ini_df = ini_df.drop(['out'], axis=1)
# new_df = prediction(ini_df)
# print(new_df.info())

#####=====----- THE END -----=====#########################################