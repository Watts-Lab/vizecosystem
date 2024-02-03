# built-in modules
from functools import reduce
from os import getenv

# venv modules
from pandas import read_csv, concat

bucket = getenv('bucket')

def load(file):
  return read_csv(f's3://{bucket}/{file}')

def concat_sets(a, b):
  # # load data
  b_data = load(b)

  # parse subset from type from file name
  file_name = b.split('_archetype_')[-1].replace('_agg_networks=True.csv', '')
  
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
  
  out_data = data\
    .melt(
      id_vars=id_cols,
      value_vars=[x for x  in data.columns if x not in id_cols],
      var_name='archetype'
    )
  
  return out_data.loc[out_data['variable'] == 'sizes']
