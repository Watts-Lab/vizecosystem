# built-in modules
from functools import reduce

# venv modules
from pandas import read_csv, concat

def load(f):
  return read_csv(f'~/Desktop/upenn/media-consumption/vizecosystem/{f}')

def concat_sets(a, b):
  # # load data
  b_data = load(b)

  # parse subset from type from file name
  file_name = b.split('_archetype_')[-1].replace('.csv', '')
  
  # assign subset columns
  b_data['variable'] = file_name

  a.append(b_data)

  return a


def parse(file):
  data = concat(
    reduce(concat_sets, file['url'][:2], []),
    ignore_index = True
  )

  id_cols = ['year', 'month', 'variable']
    
  return data\
    .melt(
      id_vars=id_cols,
      value_vars=[x for x  in data.columns if x not in id_cols],
      var_name='archetype'
    )
