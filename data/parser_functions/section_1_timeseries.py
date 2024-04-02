# built-in modules
from functools import reduce
from re import search
from os import getenv

# venv modules
from pandas import read_csv, concat, melt, merge, Grouper, DataFrame

BUCKET = getenv('BUCKET')

def load(file):
  return read_csv(f's3://{BUCKET}/{file}')

def parse_web(b):
  # load data
  b_data = load(b)

  # # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'state',  
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
  b_data = melt(
    b_data,
    id_vars=cols,
    value_vars=values,
    var_name='subset'
  )

  # # clean values
  extract_subset = b_data['subset'].str.extractall(
    r'.*\s\((?P<diet_threshold>.*)\)\s\((?P<political_lean>.*)\)\s\((?P<partisanship_scenario>.*)\)'
  )\
    .reset_index()
  # join extracted data back into b_data (using indexes)
  b_data = merge(
    b_data,
    extract_subset.loc[:,['diet_threshold', 'political_lean', 'partisanship_scenario']],
    left_index=True,
    right_index=True
  )

  # assign subset columns
  b_data['medium'] = 'web'
  # clean partisanship scenario column
  b_data['political_lean'] = b_data['political_lean'].apply(lambda x: 'left' if x == 'L' else 'right')

  return b_data.drop('subset', axis = 1)

def parse_tv(df):
  # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 'state', 
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

  # clean values
  data['diet_threshold'] = data['diet_threshold'].str.extract(r'.*\s\((.*)\)')

  return data

def concat_tv(a, b):
  # load data
  b_data = load(b)

  # filter Puerto Rico out
  b_data = b_data.loc[b_data['state'] != 'PR']

  # parse subset from file name
  # - political lean
  # - partisanship definition
  file_name = b.split('/')[1]
  political_lean, partisanship_scenario = map(
    str.lower,
    search(r'TV(.*)EchoCh(.*)_by_state.csv', file_name).group(1,2)
  )
  
  # assign subset columns
  b_data['political_lean'] = political_lean
  b_data['partisanship_scenario'] = partisanship_scenario
  b_data['medium'] = 'tv'

  # append data & return list
  a.append(b_data)

  # manually adding R Stringent values
  if ((political_lean == 'right') and (partisanship_scenario == 'lenient')):
    manual_addition = b_data.copy()
    manual_addition['partisanship_scenario'] = 'stringent'

    # append data & return list
    a.append(manual_addition)

  return a

def group_data(df, *args):
  # destructure/unpack args
  (name, max_date, min_date) = list(args)
  # initialize an empty data frame
  df_filter = DataFrame([])

  # filter depending on which subset is needed
  if (name == 'Last month'):
    df_filter = df.loc[df['timestamp'] == max_date]
  elif ('Since' in name):
    df_filter = df
  else:
    df_filter = df.loc[df['timestamp'] > min_date]
  
  # group and take the mean
  # create new column with the period information
  return df_filter.groupby([
    Grouper(key="state"),
    Grouper(key="medium"),
    Grouper(key="political_lean"),
    Grouper(key="partisanship_scenario"),
    Grouper(key="diet_threshold")
    ]
  )\
    .mean()\
    .reset_index()\
    .assign(period=name)

def parse(file):
  # loads & parses data
  # let's start with the TV dataset
  # we need to account for the fact that the R Stringent
  # file is the same as R Lenient tile, but it is not saved
  # in raw-data. We'll need to manually add those rows to
  # the data set.
  d_tv = concat(
    reduce(concat_tv, file['url'][0:3], []),
    ignore_index = True
  )
  # then we parse the web dataset,
  # which is different as it comes all 
  # #in one single file
  d_web = parse_web(file['url'][3])

  # # now we parse the TV data into what it needs to be to match the web data
  d_tv = parse_tv(d_tv)

  # # now concat web and tv together
  data = concat(
    [d_tv, d_web],
    ignore_index = True
  )

  # rename time columns
  data = data.rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)

  # pivot political lean data & return 
  return data.pivot(
      index=['year', 'month', 'state', 'medium', 'partisanship_scenario', 'diet_threshold'],
      columns='political_lean',
      values='value'
    ).reset_index()\
    .rename(columns={ 'left': 'left_pct', 'right': 'right_pct' })
