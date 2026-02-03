# built-in modules
from os import getenv

# venv modules
from pandas import read_csv

BUCKET = getenv('BUCKET')

def load(file):
  return read_csv(f's3://{BUCKET}/{file}')

def parse(file):
  data = load(file["url"])

  data['start year'] = data['start srcyearmonth'].apply(lambda x: int(x.split('-')[0]))
  data['start month'] = data['start srcyearmonth'].apply(lambda x: int(x.split('-')[1]))
  data['end year'] = data['end srcyearmonth'].apply(lambda x: int(x.split('-')[0]))
  data['end month'] = data['end srcyearmonth'].apply(lambda x: int(x.split('-')[1]))

  data = data.drop(['start srcyearmonth', 'end srcyearmonth'], axis=1)

  return data
