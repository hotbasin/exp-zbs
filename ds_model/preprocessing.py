#!/usr/bin/python3

import pandas as pd

EXCEL_FILE = 'data/anketa_demo.xlsx'
CSV_FILE = 'data/anketa_demo.csv'

demo_df = pd.read_excel(EXCEL_FILE)

old_cols = [
    'Отметка времени',
    'Профиль телеграмм (в формате @username)',
    'Часовой пояс',
    'Стек технологий',
    'По какой специальности SF хотите заявиться?',
    'Роль',
    'В какой роли видите себя в проекте?',
    'Сколько часов в неделю готовы уделять проекту?',
    'Какие другие курсы закончили или находитесь в процессе обучения?',
    'Как долго учитесь на курсах?',
    'Notes',
    'ЯП',
    'Вступление в чат практики.',
    'Выбыл'
]
new_cols = [
    'date',
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
    'out'
]

#####=====----- THE END -----=====#########################################