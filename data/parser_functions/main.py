# built-in modules
from functools import reduce
from os import getenv

# venv modules
from pandas import read_csv, melt, concat

bucket = getenv('bucket')

def load(file):
  return read_csv(f's3://{bucket}/{file}')

def parse_tv(d):
    # clean NaNs
    d['age_group'] = d['age_group'].fillna('All')
    d['gender'] = d['gender'].fillna('All')
    d['state'] = d['state'].fillna('US')

    # replace values 1/2 values for gender
    d['gender'] = d['gender'].replace({ 1: 'Male', 2: 'Female' })

    cols = [
      'activityyear',
      'activitymonth',
      'state',
      'gender',
      'age_group'
    ]

    values = [
      'avg news mins / person / day',
      'avg non-news mins / person / day'
    ]

    d = melt(
      d,
      id_vars=cols,
      value_vars=values,
      var_name='category'
    )

    d['category'] = d['category']\
      .str.extract(r'avg (.*)[_|\s]mins \/ person \/ day')

    d.loc[:,'medium'] = 'tv'

    return d

def parse_web(d):
    # # clean NaNs
    d['age_group'] = d['age_group'].fillna('All')
    d['gender'] = d['gender_id'].fillna('All')
    d['state'] = d['state'].fillna('US')

    # # replace values 1/2 values for gender
    d['gender'] = d['gender'].replace({ 1: 'Male', 2: 'Female' })
    d = d.drop('gender_id', axis = 1)

    cols = [
      'activityyear',
      'activitymonth',
      'state',
      'gender',
      'age_group'
    ]

    values = [
      'avg hard_news_mins / person / day',
      'avg fake_news_mins / person / day',
      'avg facebook_mins / person / day',
      'avg twitter_mins / person / day',
      'avg youtube_mins / person / day',
      'avg reddit_mins / person / day',
      'avg ALL_mins / person / day'
    ]

    calculated_category = 'avg non_news_mins / person / day'

    d.loc[:, calculated_category] = d.loc[:, values[-1]] - d.loc[:, values[:-1]].apply(sum, axis = 1)

    d = melt(
      d,
      id_vars=cols,
      value_vars=values + [calculated_category],
      var_name='category'
    )

    d = d.loc[d['category'] != values[-1]]

    d['category'] = d['category']\
      .str.extract(r'avg (.*)[_|\s]mins \/ person \/ day')

    d.loc[:,'medium'] = 'web'

    return d

def concat_tv(a, b):
  # load data
  b_data = load(b)

  # # append data & return list
  a.append(b_data)

  return a

def concat_web(a, b):
  # load data
  b_data = load(b)

  # append data & return list
  a.append(b_data)

  return a

def parse(file):
  # # # loads & parses data
  # # # let's start with the TV dataset
  d_tv = concat(
    reduce(concat_tv, file['url'][:5], []),
    ignore_index = True
  )
  d_tv = parse_tv(d_tv)

  # # # now we do the same for the web data
  d_web = concat(
    reduce(concat_web, file['url'][5:], []),
    ignore_index = True
  )
  d_web = parse_web(d_web)

  # and we put those 2 together
  d = concat([d_tv, d_web]) 

  return d.rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)
