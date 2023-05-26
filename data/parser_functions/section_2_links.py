# built-in modules
from functools import reduce
from re import search

# venv modules
from pandas import read_csv, concat, melt, merge

def load(f):
  return read_csv(f)

def parse(file):
  data = load(f'~/Documents/felippe/upenn/media-consumption/vizecosystem/{file["url"]}')

  return data.drop('Unnamed: 0', axis = 1)\
    .pivot(
      index=['start year', 'start month', 'end year', 'end month', 'from node'],
      columns='to node',
      values='net flow'
    ).reset_index()\
    .rename({ 'from node': 'from' }, axis=1)
