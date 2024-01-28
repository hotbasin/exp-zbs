import category_encoders as ce
import pickle
import pandas as pd
import numpy as np

from sklearn import model_selection
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from imblearn.over_sampling import SMOTE


  # Дата-время
def to_predict(row):
  data=row
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
  data['period_of_day'].value_counts()
  date_df_dum = pd.get_dummies(date_df, columns=['day_name', 'period_of_day'])

  # ЯП
  data['language'].fillna('нуль')
  def get_java(x):
    if str(x).lower() == 'js':
      return 'java'
    else:
      return str(x).lower()

  data['language'] = data['language'].apply(get_java)

  languages = [
      'python',
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

  for lang in languages:
      data[lang] = data['language'].apply(
          lambda x: 1 if lang in str(x).lower() else 0
      )


  # Роль

  def get_role(x):
      if 'backend' in str(x).lower() or 'back' in str(x).lower() or 'бэк' in str(x).lower():
          return 'backend'
      elif 'frontend' in str(x).lower() or 'front' in str(x).lower() or 'фронт' in str(x).lower():
          return 'frontend'
      elif 'аналит' in str(x).lower() or 'analys' in str(x).lower() or 'ba' in str(x).lower():
          return 'аналитик'
      elif 'ds' in str(x).lower() or 'scient' in str(x).lower():
          return 'data scientist'
      elif 'дизайн' in str(x).lower() or \
          'design' in str(x).lower() or \
          'UX' in str(x).lower():
          return 'дизайнер'
      elif 'project' in str(x).lower() or 'проект' in str(x).lower():
          return 'project manager'
      elif 'android' in str(x).lower():
          return 'android'
      elif 'ios' in str(x).lower():
          return 'ios'
      elif 'full' in str(x).lower() or\
          'develop' in str(x).lower() or\
          'разраб' in str(x).lower() or \
          'программ' in str(x).lower():
          return 'fullstack'
      elif 'админ' in str(x).lower():
          return 'системный администратор'
      elif 'dev' in str(x).lower():
          return 'devops'
      elif 'qa' in str(x).lower() or 'тест' in str(x).lower() or 'test' in str(x).lower():
          return 'тестировщик'
      else:
          return 'other'

  data['role_in_new'] = data['role_in'].apply(get_role)
  data['test_role'] = data['role'].apply(get_role)

  def to_compar(row):
      if str(row['test_role']).lower() == str(row['role_in_new']).lower():
          return 1
      else:
          return 0

  data['compar_role'] = data.apply(to_compar, axis=1)

  # Время на практику
  def get_time(x):
      if '10+ часов' in x:
          return 0
      if '20+ часов' in x:
          return 1
      if 'готов работать 25/8' in x:
          return 2

  data['time_par_week'] = data['hour_per_week'].apply(get_time)

  # Чистка и кодирование
  df = pd.get_dummies(data, columns=['day_name', 'period_of_day'])
  df = df.drop(['hour_of_day', 'qa', 'role_in', 'notes'], axis=1)

  bin_encoder = ce.BinaryEncoder(cols=['role', 'role_in'])
  bin = bin_encoder.fit_transform(data[['role', 'role_in']])
  df = pd.concat([df, bin], axis=1)
  
  object_columns = [s for s in df.columns if df[s].dtypes == 'object']
  df.drop(object_columns, axis = 1, inplace=True)

  X = df.drop(['out', 'date'], axis=1)
  y = df['out']

  X_train, X_valid, y_train, y_valid = model_selection.train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42)
  
  sm = SMOTE(random_state=42)
  X_train_s, y_train_s = sm.fit_resample(X_train, y_train)
  
  return X_train_s, y_train_s

X, y = to_predict(data)

with open('test_pipe.pkl', 'rb') as pkl_file:
    test_model = pickle.load(pkl_file)
    test_model

predict = pd.DataFrame(test_model.predict_proba(X)[:, 1])

threshold_lg = 0.4

y_class = predict[0].apply(lambda x: 1 if x > threshold_lg else 0)
predict_df = pd.concat([data['id'], predict, y_class], axis=1)
predict_df.columns = ['id', 'predict_prob', 'predict_class']