# built-in modules
from re import search
from os import getenv

# venv modules
from pandas import read_csv, concat, to_datetime, Grouper

bucket = getenv('bucket')

def load(file):
  return read_csv(f's3://{bucket}/{file}')

def get_top_n(x, n, val):
  return x.sort_values(val, ascending=False)\
    .groupby(Grouper('state'))\
    .head(n)

def format_df(file):
  d = load(file)

  # if file contains date info, filter for just last month
  time_cols = ['activityyear', 'activitymonth']
  if any([x in d.columns for x in time_cols]):
    counts = d.loc[:,time_cols]\
      .value_counts()\
      .reset_index()\
      .assign(day=1)
    
    dates = to_datetime(dict(year = counts[time_cols[0]], month = counts[time_cols[1]], day = counts['day']))

    max_date = max(dates)
    max_year = max_date.year
    max_month = max_date.month
    
    d = d[
      (d[time_cols[0]] == max_year) & (d[time_cols[1]] == max_month)
    ]

  # get what subset this is
  period = search(
    r'.*_by_state_(.*)_top_.*', file
  )\
    .group(1)\
    .replace('_', ' ')\
    .replace('last since 2016', 'since 2016')
    
  d['period'] = period.capitalize()

  return d

def parse_tv(file):
  values = 'audience_size_est_30'
  cols = [
    'state',
    'program_name',
    'network',
    'period',
  ]
  d = [
    format_df(f).sort_values(values, ascending = False) 
    for f in file
  ]
  d = concat([get_top_n(f, 10, values) for f in d])

  # # # keep only needed columns
  return d.loc[d['state'] != 'PR', cols + [values]]\
    .assign(medium='tv')\
    .rename({ values: 'value', 'program_name': 'program' }, axis = 1)

def parse_web(file):
  values = 'audience_size_est_1'
  cols = [
    'state',
    'domain',
    'period',
  ]
  d = [
    format_df(f).sort_values(values, ascending = False) 
    for f in file
  ]
  d = concat([get_top_n(f, 10, values) for f in d])

  # # # keep only needed columns
  return d.loc[d['state'] != 'PR', cols + [values]]\
    .assign(medium='web')\
    .rename({ values: 'value' }, axis = 1)

def parse(file):
  d_tv = parse_tv(file['url'][:4])
  d_web = parse_web(file['url'][4:])

  return concat([d_tv, d_web])