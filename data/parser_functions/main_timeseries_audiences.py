# built-in modules
from functools import reduce
from re import search

# venv modules
from pandas import read_csv, concat, melt, to_datetime, Grouper, DataFrame
from pandas.tseries.offsets import DateOffset

# local modules
import enforce_order

def load(f):
  return read_csv(f'~/Documents/felippe/upenn/media-consumption/vizecosystem/{f}')

def get_top_n(x, n, val):
  return x.sort_values(val, ascending=False)\
    .groupby(Grouper('state'))\
    .head(n)

def format_df(file):
  d = load(file)

  # if file contains date info, filt for just last month
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
    r'news_program_ranked_by_audiences_agg=(.*)_dem.*', file
  )\
    .group(1)\
    .replace('_', ' ')\
    .replace('monthly', 'Last month')\
    
  d['period'] = period

  return d

def parse(file):
  values = 'audience_size_est_60'
  cols = [
    'state',
    'program_name',
    'network',
    'period',
  ]
  d = [
    format_df(f).sort_values(values, ascending = False) 
    for f in file['url']
  ]
  d = concat([get_top_n(f, 10, values) for f in d])
  
  # # # keep only needed columns
  return d.loc[d['state'] != 'PR', cols + [values]]\
    .assign(medium='tv')\
    .rename({ values: 'value', 'program_name': 'program' }, axis = 1)
