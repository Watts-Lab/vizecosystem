# built-in modules
from functools import reduce
from re import search
from os import getenv

# venv modules
from pandas import read_csv, concat, merge, melt, to_datetime, Grouper, DataFrame, DateOffset
from pandas.tseries.offsets import DateOffset

bucket = getenv('bucket')

def load(file):
  return read_csv(f's3://{bucket}/{file}')

def parse_web_frac(d):
  # # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'state',  
  ]
  values = [
    'frac of weights (50) (R) (lenient)',
    'frac of weights (50) (R) (stringent)',
    'frac of weights (50) (L) (lenient)',
    'frac of weights (50) (L) (stringent)',
  ]
  # # unpivot data
  frac_data = melt(
    d,
    id_vars=cols,
    value_vars=values,
    var_name='subset'
  )

  # # clean values
  extract_subset = frac_data['subset'].str.extractall(
    r'.*\s\((?P<diet_threshold>.*)\)\s\((?P<political_lean>.*)\)\s\((?P<partisanship_scenario>.*)\)'
  )\
    .reset_index()
  # join extracted data back into b_data (using indexes)
  frac_data = merge(
    frac_data,
    extract_subset.loc[:,['diet_threshold', 'political_lean', 'partisanship_scenario']],
    left_index=True,
    right_index=True
  )

  # assign subset columns
  frac_data['medium'] = 'web'
  # clean partisanship scenario column
  frac_data['political_lean'] = frac_data['political_lean'].apply(lambda x: 'left' if x == 'L' else 'right')

  return frac_data.drop('subset', axis = 1)

def parse_web_size(d):
  # # keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'state',  
  ]
  values = [
    'weighted_count_r_ec_50',
    # 'weighted_count_r_ec_75',
    'weighted_count_fr_ec_50',
    # 'weighted_count_fr_ec_75',
    'weighted_count_l_ec_50',
    # 'weighted_count_l_ec_75',
    'weighted_count_fl_ec_50',
    # 'weighted_count_fl_ec_75'
  ]
  # # unpivot data
  size_data = melt(
    d,
    id_vars=cols,
    value_vars=values,
    value_name='size',
    var_name='subset'
  )

  # # clean values
  extract_subset = size_data['subset'].str.extractall(
    r'weighted_count_(?P<political_lean>.*)_.*_(?P<diet_threshold>.*)'
  )\
    .reset_index()
  # join extracted data back into b_data (using indexes)
  size_data = merge(
    size_data,
    extract_subset.loc[:,['diet_threshold', 'political_lean']],
    left_index=True,
    right_index=True
  )

  partisan_political_map = {
    'l': { 'partisanship': 'lenient', 'political': 'left' },
    'r': { 'partisanship': 'lenient', 'political': 'right' },
    'fl': { 'partisanship': 'stringent', 'political': 'left' },
    'fr': { 'partisanship': 'stringent', 'political': 'right' }
  }

  # assign subset columns
  size_data['medium'] = 'web'
  # # add lenient & stringent scenario
  size_data['partisanship_scenario'] = size_data['political_lean'].apply(lambda x: partisan_political_map[x]['partisanship'])
  # # clean partisanship scenario column
  size_data['political_lean'] = size_data['political_lean'].apply(lambda x: partisan_political_map[x]['political'])

  return size_data.drop('subset', axis = 1)

def parse_web(b):
  # load data
  b_data = load(b)

  frac_data = parse_web_frac(b_data)
  size_data = parse_web_size(b_data)
  
  return merge(
    frac_data,
    size_data,
    on=['activityyear', 'activitymonth', 'state', 'diet_threshold', 'political_lean', 'medium', 'partisanship_scenario']
  )

def parse_tv_frac(d):
  #  keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 'state', 
    'political_lean', 'partisanship_scenario'
  ]
  values = [
    'frac of weights (50)', 
    # 'frac of weights (75)'
  ]

  # unpivot data
  data = melt(
    d,
    id_vars=cols,
    value_vars=values,
    var_name='diet_threshold'
  )

  # clean values
  data['diet_threshold'] = data['diet_threshold'].str.extract(r'.*\s\((.*)\)')
  
  return data

def parse_tv_size(d):
  #  keep only needed columns
  cols = [
    'activityyear', 'activitymonth', 'medium', 'state', 
    'political_lean', 'partisanship_scenario'
  ]
  values = [
    'weighted_count_50', 
    # 'weighted_count_75'
  ]

  # unpivot data
  data = melt(
    d,
    id_vars=cols,
    value_vars=values,
    value_name='size',
    var_name='diet_threshold'
  )

  # clean values
  data['diet_threshold'] = data['diet_threshold'].str.extract(r'weighted_count_(.*)')
  
  return data

def parse_tv(df):
  frac_data = parse_tv_frac(df)
  size_data = parse_tv_size(df)

  data = merge(
    frac_data,
    size_data,
    on=['activityyear', 'activitymonth', 'state', 'diet_threshold', 'political_lean', 'medium', 'partisanship_scenario']
  )

  return data

def concat_tv(a, b):
  # load data
  b_data = load(b)

  # # if TV:
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
  # # loads & parses data
  # # let's start with the TV dataset
  # # we need to account for the fact that the R Stringent
  # # file is the same as R Lenient file, but it is not saved
  # # in raw-data. We'll need to manually add those rows to
  # # the data set.
  d_tv = concat(
    reduce(concat_tv, file['url'][0:3], []),
    ignore_index = True
  )
  # # then we parse the web dataset,
  # # which is different as it comes all 
  # # in one single file
  d_web = parse_web(file['url'][3])

  # # # now we parse the TV data into what it needs to be to match the web data
  d_tv = parse_tv(d_tv)

  # # # for each subset, we need to perform a bunch of transformations
  # # # let's crete a holder to concat subsets together at the end
  subsets = []
  for d in [d_tv, d_web]:
    # # # filter Puerto Rico & VI out
    data = d.loc[(d['state'] != 'PR') & (d['state'] != 'VI')]

    # # # add timestamp column to data
    data['timestamp'] = to_datetime(data.apply(lambda x: f"{x['activityyear']}-{x['activitymonth']}", axis=1), format='%Y-%m')

    # # # remove unused columns
    data = data.drop(['activityyear', 'activitymonth'], axis=1)

    # # # create pairs of data. these are the bounds we're gonna use as a filter
    # # # to aggregate temporaly
    last_date = data['timestamp'].max()
    first_date = data['timestamp'].min()
    bounds = [
      # ('Last month', last_date, last_date),
      ('Last 3 months', last_date, last_date - DateOffset(months=3)),
      ('Last 6 months', last_date, last_date - DateOffset(months=6)),
      ('Last 12 months', last_date, last_date - DateOffset(months=12)),
      (f'Since {first_date.strftime("%Y")}', last_date, first_date)
    ]

    # # # filter and group data according to bounds set above
    # # # we call *x so that the tuple is passed to the 
    # # # function as args that can be destructured/unpacked
    grouped_data = concat(
      [group_data(data, *x) for x in bounds],
      ignore_index = True
    )\
    .pivot(
      # # pivot political lean data
      index=['period', 'state', 'medium', 'partisanship_scenario', 'diet_threshold'],
      columns='political_lean',
      values=['value', 'size']
    )
    # then transform multi-level cols into single level cols
    grouped_data.columns = ['_'.join(col) for col in grouped_data.columns.values]

    subsets.append(grouped_data)

  # # # now concat web and tv together
  out_data = concat(
    subsets,
    ignore_index = False
  )

  # rename cols, reset index & return
  return out_data.rename(
    columns={ 
      'value_left': 'left_pct', 
      'value_right': 'right_pct',
      'size_left': 'left_size',
      'size_right': 'right_size'
    }
  )\
  .reset_index()
