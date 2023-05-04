# built-in modules
from functools import reduce
from re import search

# venv modules
from pandas import read_csv, concat, melt, merge

# # local modules
# import enforce_order

def load(f):
  return read_csv(f)

def parse_web(df):
  # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 
    'gender', 'age_group'
  ]
  values = [
    'frac of weights (50) (R) (lenient)',
    'frac of weights (75) (R) (lenient)',
    'frac of weights (50) (R) (stringent)',
    'frac of weights (75) (R) (stringent)',
    'frac of weights (50) (L) (lenient)',
    'frac of weights (75) (L) (lenient)',
    'frac of weights (50) (L) (stringent)',
    'frac of weights (75) (L) (stringent)'
  ]
  # # unpivot data
  data = melt(
    df,
    id_vars=cols,
    value_vars=values,
    var_name='subset'
  )

  # # clean values
  extract_subset = data['subset'].str.extractall(
    r'.*\s\((?P<diet_threshold>.*)\)\s\((?P<political_lean>.*)\)\s\((?P<partisanship_scenario>.*)\)'
  )\
    .reset_index()
  # join extracted data back into b_data (using indexes)
  data = merge(
    data,
    extract_subset.loc[:,['diet_threshold', 'political_lean', 'partisanship_scenario']],
    left_index=True,
    right_index=True
  )

  # assign subset columns
  data['medium'] = 'web'

  return data.drop('subset', axis = 1)

def parse_tv(df):
  # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 
    'gender', 'age_group',
    'political_lean', 'partisanship_scenario'
  ]
  values = ['frac of weights (50)', 'frac of weights (75)']

  # unpivot data
  data = melt(
    df,
    id_vars=cols,
    value_vars=values,
    var_name='diet_threshold'
  )

  # # clean values
  data['diet_threshold'] = data['diet_threshold'].str.extract(r'.*\s\((.*)\)')
  data = data.replace({ "political_lean": { 'left': 'L', 'right': 'R' } })

  return data


def concat_web(a, b):
  # # load data
  b_data = load(f'~/Documents/felippe/upenn/media-consumption/vizecosystem/{b}')

  # parse subset from type from file name
  file_name = b.split('_')[-1].replace('.csv', '')
  
  # assign subset columns
  b_data['medium'] = 'web'

  if file_name == 'adults':
    b_data['age_group'] = 'All'
    b_data['gender'] = 'All'
  elif file_name == 'age':
    b_data['gender'] = 'All'
  else: 
    b_data['age_group'] = 'All'
    b_data['gender'] = b_data['gender_id'].replace({ 1: 'Male', 2: 'Female' })
    b_data = b_data.drop('gender_id', axis = 1)

  a.append(b_data)

  return a

def concat_tv(a, b):
  # # load data
  b_data = load(f'~/Documents/felippe/upenn/media-consumption/vizecosystem/{b}')

  # parse subset from file name
  # - political lean
  # - partisanship definition
  file_name = b.split('/')[1]

  political_lean, partisanship_scenario, file_type = map(
    str.lower,
    search(r'TV(.*)EchoCh(.*)_.*_(.*).csv', file_name).group(1, 2, 3)
  )
  
  # assign subset columns
  b_data['political_lean'] = political_lean
  b_data['partisanship_scenario'] = partisanship_scenario
  b_data['medium'] = 'tv'

  if file_type == 'adults':
    b_data['age_group'] = 'All'
    b_data['gender'] = 'All'
  elif file_type == 'age':
    b_data['gender'] = 'All'
  else: 
    b_data['age_group'] = 'All'
    b_data['gender'] = b_data['gender'].replace({ 1: 'Male', 2: 'Female' })
  
  # append data & return list
  a.append(b_data)

  # manually adding R Stringent values
  if ((political_lean == 'right') and (partisanship_scenario == 'lenient')):
    manual_addition = b_data.copy()
    manual_addition['partisanship_scenario'] = 'stringent'

    # append data & return list
    a.append(manual_addition)

  return a

def parse(file):
  # loads & parses data
  # let's start with the TV dataset
  # we need to account for the fact that the R Stringent
  # file is the same as R Lenient file, but it is not saved
  # in raw-data. We'll need to manually add those rows to
  # the data set.
  d_tv = concat(
    reduce(concat_tv, file['url'][0:9], []),
    ignore_index = True
  )

  d_tv = parse_tv(d_tv)

  # then we parse the web dataset,
  # which is different as it comes all 
  # #in one single file
  d_web = concat(
    reduce(concat_web, file['url'][9:], []),
    ignore_index = True
  )

  d_web = parse_web(d_web)

  # # now concat web and tv together
  data = concat(
    [d_tv, d_web],
    ignore_index = True
  )

  # rename time columns
  data = data.rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)

  return data
