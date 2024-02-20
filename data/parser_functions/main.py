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
    d['race'] = d['race'].fillna('All')
    d['state'] = d['state'].fillna('US')

    # replace values 1/2 values for gender
    d['gender'] = d['gender'].replace({ 1: 'Male', 2: 'Female' })

    cols = [
      'activityyear',
      'activitymonth',
      'state',
      'gender',
      'age_group',
      'race'
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
    d['race'] = d['race'].fillna('All')
    d['state'] = d['state'].fillna('US')

    # # replace values 1/2 values for gender
    d['gender'] = d['gender'].replace({ 1: 'Male', 2: 'Female' })
    d = d.drop('gender_id', axis = 1)
    d['race'] = d['race'].replace({ 'white': 'white+other', 'other': 'white+other' })

    cols = [
      'activityyear',
      'activitymonth',
      'state',
      'gender',
      'age_group',
      'race'
    ]

    values = [
      'avg hard_news_mins / person / day',
      'avg fake_news_mins / person / day',
      'avg social_media_mins / person / day',
      'avg ALL_mins / person / day'
    ]

    calculated_category = 'avg non_news_mins / person / day'

    d.loc[:, calculated_category] = d.loc[:, values[-1]] - d.loc[:, values[:-1]].apply(sum, axis = 1)

    d = d[cols + values + [calculated_category]].groupby(cols, as_index=False).sum()

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

def parse_mob(d):
    # # clean NaNs
    d['age_group'] = d['age_group'].fillna('All')
    d['gender'] = d['gender'].fillna('All')
    d['race'] = d['race'].fillna('All')
    d['state'] = d['state'].fillna('US')

    # # replace values 1/2 values for gender
    d['gender'] = d['gender'].replace({ 'M': 'Male', 'F': 'Female' })
    d['race'] = d['race'].replace({ 'white': 'white+other', 'other': 'white+other' })

    cols = [
      'activityyear',
      'activitymonth',
      'state',
      'gender',
      'age_group',
      'race'
    ]

    values = [
      'avg social_media / person / day',
      'avg entertainment / person / day',
      'avg utility / person / day',
      'avg communication / person / day',
      'avg news / person / day',
      'avg lifestyle / person / day',
      'avg unlabeled_app / person / day',
      'avg browser / person / day',
    ]

    d = melt(
      d,
      id_vars=cols,
      value_vars=values,
      var_name='category'
    )

    d['category'] = d['category']\
      .str.extract(r'avg (.*) \/ person \/ day')

    d.loc[:,'medium'] = 'mobile'

    return d

def concat_files(a, b):
  # load data
  b_data = load(b)

  # # append data & return list
  a.append(b_data)

  return a

def parse(file):
  # # # loads & parses data
  # # # let's start with the TV dataset
  d_tv = concat(
    reduce(concat_files, file['url'][:8], []),
    ignore_index = True
  )
  d_tv = parse_tv(d_tv)

  # # # now we do the same for the web data
  d_web = concat(
    reduce(concat_files, file['url'][8:16], []),
    ignore_index = True
  )
  d_web = parse_web(d_web)

  d_mob = concat(
    reduce(concat_files, file['url'][16:], []),
    ignore_index = True
  )

  d_mob = parse_mob(d_mob)

  # # # # and we put those 2 together
  d = concat([d_tv, d_web, d_mob]) 

  return d.rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)
