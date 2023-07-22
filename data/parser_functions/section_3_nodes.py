# built-in modules
from functools import reduce
from re import search

# venv modules
from pandas import read_csv, concat, melt, merge

def load(f):
  return read_csv(f)

def concat_sets(a, b):
  # # load data
  b_data = load(f'~/Desktop/upenn/media-consumption/vizecosystem/{b}')

  # parse subset from type from file name
  file_name = b.split('_archetype_')[-1].replace('.csv', '')
  
  # assign subset columns
  b_data['variable'] = file_name

  a.append(b_data)

  return a


def parse(file):
  data = concat(
    reduce(concat_sets, file['url'], []),
    ignore_index = True
  )

  id_cols = ['year', 'month', 'variable']

  # data = data.drop('Unnamed: 0', axis = 1)
    
  return data\
    .melt(
      id_vars=id_cols,
      value_vars=[x for x  in data.columns if x not in id_cols],
      var_name='archetype'
    )

