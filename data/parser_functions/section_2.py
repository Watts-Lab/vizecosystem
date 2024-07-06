# built-in modules
from functools import reduce
from re import search
from os import getenv

# venv modules
from pandas import read_csv, concat, melt, merge

BUCKET = getenv('BUCKET')

def load(file):
  return read_csv(f's3://{BUCKET}/{file}')

def parse_web(df):
  # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 
    'gender', 'age_group', 'ethnicity',
  ]
  subsets = ['diet_threshold', 'political_lean', 'partisanship_scenario']
  val_keys = [
    'weighted_count_r_ec_50',
    'weighted_count_fr_ec_50',
    'weighted_count_r_ec_75',
    'weighted_count_fr_ec_75',
    'weighted_count_l_ec_50',
    'weighted_count_fl_ec_50',
    'weighted_count_l_ec_75',
    'weighted_count_fl_ec_75',
  ]
  new_keys = [
    'frac of weights (50) (R) (lenient)',
    'frac of weights (50) (R) (stringent)',
    'frac of weights (75) (R) (lenient)',
    'frac of weights (75) (R) (stringent)',
    'frac of weights (50) (L) (lenient)',
    'frac of weights (50) (L) (stringent)',
    'frac of weights (75) (L) (lenient)',
    'frac of weights (75) (L) (stringent)',
  ]
  denom = 'weighted_count_denom'

  df = df.loc[:,cols+val_keys+[denom]]\
    .replace({ 'white': 'white+other', 'other': 'white+other' })\
    .groupby(by=cols)\
    .sum()\
    .reset_index()

  totals = df.loc[:,val_keys]
  denoms = df.loc[:,denom]
  values = totals.div(denoms.values, axis=0)
   
  df = concat([df.loc[:,cols], values], axis=1)\
    .rename(
      {val_keys[k]: new_keys[k] for k in [i for i, x in enumerate(val_keys)]}, 
      axis=1 
    )
  # unpivot data
  data = melt(
    df,
    id_vars=cols,
    value_vars=new_keys,
    var_name='subset'
  )

  # # clean values
  extract_subset = data['subset'].str.extractall(
    r'.*\s\((?P<diet_threshold>.*)\)\s\((?P<political_lean>.*)\)\s\((?P<partisanship_scenario>.*)\)'
  )\
    .reset_index(drop=True)
  
  # join extracted data back into data (using indexes)
  data = merge(
    data,
    extract_subset.loc[:,subsets],
    left_index=True,
    right_index=True
  )

  return data[cols+subsets+['value']]

def parse_tv(df):
  # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 
    'gender', 'age_group', 'ethnicity',
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
  b_data = load(b)

  # parse subset from type from file name
  file_name = b.split('/')[1].split('_sizes_')[-1].replace('.csv', '')
  
  # # assign subset columns
  b_data['medium'] = 'web'

  if file_name == 'all_adults':
    b_data['age_group'] = 'All'
    b_data['gender'] = 'All'
    b_data['ethnicity'] = 'All'
  elif file_name == 'by_age':
    b_data['gender'] = 'All'
    b_data['ethnicity'] = 'All'
  elif file_name == 'by_gender':
    b_data['age_group'] = 'All'
    b_data['ethnicity'] = 'All'
    b_data['gender'] = b_data['gender_id'].replace({ 1: 'Male', 2: 'Female' })
  elif file_name == 'by_race':
    b_data['age_group'] = 'All'
    b_data['ethnicity'] = b_data['race']
    b_data['gender'] = 'All'
  elif file_name == 'by_age_x_gender':
    b_data['ethnicity'] = 'All'
    b_data['gender'] = b_data['gender_id'].replace({ 1: 'Male', 2: 'Female' })
  elif file_name == 'by_age_x_race':
    b_data['gender'] = 'All'
    b_data['ethnicity'] = b_data['race']
  elif file_name == 'by_gender_x_race':
    b_data['age_group'] = 'All'
    b_data['gender'] = b_data['gender_id'].replace({ 1: 'Male', 2: 'Female' })
    b_data['ethnicity'] = b_data['race']
  
  if 'gender_id' in b_data.columns: 
    b_data = b_data.drop('gender_id', axis = 1)

  a.append(b_data)

  return a

def concat_tv(a, b):
  # # load data
  b_data = load(b)
  # parse subset from file name
  # - political lean
  # - partisanship definition
  file_name = b.split('/')[1]

  political_lean, partisanship_scenario, file_type = map(
    str.lower,
    search(r'TV(.*)EchoCh(.*?)_b?y?_?(.*).csv', file_name).group(1, 2, 3)
  )

  # # # assign subset columns
  b_data['political_lean'] = political_lean
  b_data['partisanship_scenario'] = partisanship_scenario
  b_data['medium'] = 'tv'
  

  if file_type == 'all_adults':
    b_data['age_group'] = 'All'
    b_data['gender'] = 'All'
    b_data['ethnicity'] = 'All'
  elif file_type == 'age':
    b_data['gender'] = 'All'
    b_data['ethnicity'] = 'All'
  elif file_type == 'gender':
    b_data['age_group'] = 'All'
    b_data['gender'] = b_data['gender'].replace({ 1: 'Male', 2: 'Female' })
    b_data['ethnicity'] = 'All'
  elif file_type == 'race':
    b_data['gender'] = 'All'
    b_data['age_group'] = 'All'
    b_data['ethnicity'] = b_data['race']
  elif file_type == 'age_x_race':
    b_data['gender'] = 'All'
    b_data['ethnicity'] = b_data['race']
  elif file_type == 'gender_x_race':
    b_data['age_group'] = 'All'
    b_data['gender'] = b_data['gender'].replace({ 1: 'Male', 2: 'Female' })
    b_data['ethnicity'] = b_data['race']
  elif file_type == 'age_x_gender':
    b_data['ethnicity'] = 'All'
    b_data['gender'] = b_data['gender'].replace({ 1: 'Male', 2: 'Female' })

  # # append data & return list
  a.append(b_data)

  # # manually adding R Stringent values
  if ((political_lean == 'right') and (partisanship_scenario == 'lenient')):
    manual_addition = b_data.copy()
    manual_addition['partisanship_scenario'] = 'stringent'

    # append data & return list
    a.append(manual_addition)

  return a

def parse(file):
  # # loads & parses data
  # # let's start with the TV dataset
  # # we need to account for the fact that the R Stringent
  # # file is the same as R Lenient file, but it is not saved
  # # in raw-data. We'll need to manually add those rows to
  # # the data set.
  d_tv = concat(
    reduce(concat_tv, file['url'][0:21], []),
    ignore_index = True
  )

  d_tv = parse_tv(d_tv)

  # # then we parse the web dataset,
  # # which is different as it comes all 
  # # #in one single file
  d_web = concat(
    reduce(concat_web, file['url'][21:], []),
    ignore_index = True
  )

  d_web = parse_web(d_web)

  # # # now concat web and tv together
  data = concat(
    [d_tv, d_web],
    # [d_web],
    ignore_index = True
  )

  # rename time columns
  data = data.rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)

  # return data
  return data