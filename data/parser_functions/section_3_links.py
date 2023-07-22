# built-in modules
from functools import reduce
from re import search

# venv modules
from pandas import read_csv

def load(f):
  return read_csv(f)

def parse(file):
  data = load(f'~/Desktop/upenn/media-consumption/vizecosystem/{file["url"]}')

  return data\
    .pivot(
      index=['start year', 'start month', 'end year', 'end month', 'from node'],
      columns='to node',
      values='net flow'
    ).reset_index()\
    .rename({ 'from node': 'from' }, axis=1)
