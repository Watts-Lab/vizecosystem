# built-in modules
from os import getenv

# venv modules
from pandas import read_csv

BUCKET = getenv('BUCKET')

def load(file):
  return read_csv(f's3://{BUCKET}/{file}')

def parse(file):
  data = load(file["url"])

  return data\
    .pivot(
      index=['start year', 'start month', 'end year', 'end month', 'from node'],
      columns='to node',
      values='net flow'
    ).reset_index()\
    .rename({ 'from node': 'from' }, axis=1)
