# built-in modules
from functools import reduce
from os import getenv

# venv modules
from pandas import read_csv, melt, concat

BUCKET = getenv('BUCKET')

def load(file):
  return read_csv(f's3://{BUCKET}/{file}')

def concat_files(a, b):
  # load data
  b_data = load(b)

  # # append data & return list
  a.append(b_data)

  return a

def lower_case(df):
  df.columns = map(str.lower, df.columns)
  
  return df

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
    'avg entertainment mins / person / day',
    'avg documentary mins / person / day',
    'avg reality_variety mins / person / day',
    'avg sports mins / person / day',
    'avg other mins / person / day'
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
    'avg entertainment_mins / person / day',
    'avg other_mins / person / day'
  ]

  calculated_categories = {
    'avg lifestyle_mins / person / day': [   
      'avg retail_mins / person / day',
      'avg lifestyle_mins / person / day',   
    ]
  }

  for category, sub_categories in calculated_categories.items():
    d.loc[:, category] = d.loc[:, sub_categories].apply(sum, axis = 1)

  calculated_categories_cols = list(calculated_categories.keys())

  d = d[cols + values + calculated_categories_cols].groupby(cols, as_index=False).sum()

  d = melt(
    d,
    id_vars=cols,
    value_vars=values + calculated_categories_cols,
    var_name='category'
  )

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
    'avg news / person / day',    
  ]

  calculated_categories = {
    'avg other / person / day': [   
      'avg unlabeled_app / person / day',
      'avg browser / person / day',
      'avg communication / person / day',
    ],
    'avg lifestyle / person / day': [  
      'avg utility / person / day',
      'avg lifestyle / person / day',
    ],
  }

  for category, sub_categories in calculated_categories.items():
    d.loc[:, category] = d.loc[:, sub_categories].apply(sum, axis = 1)

  calculated_categories_cols = list(calculated_categories.keys())

  d = d[cols + values + calculated_categories_cols].groupby(cols, as_index=False).sum()

  d = melt(
    d,
    id_vars=cols,
    value_vars=values + calculated_categories_cols,
    var_name='category'
  )

  d['category'] = d['category']\
    .str.extract(r'avg (.*) \/ person \/ day')

  d.loc[:,'medium'] = 'mobile'

  return d

def parse_tab(d):
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
    'avg news / person / day',    
  ]

  calculated_categories = {
    'avg other / person / day': [   
      'avg unlabeled_app / person / day',
      'avg browser / person / day',
      'avg communication / person / day',
    ],
    'avg lifestyle / person / day': [  
      'avg utility / person / day',
      'avg lifestyle / person / day',
    ],
  }

  for category, sub_categories in calculated_categories.items():
    d.loc[:, category] = d.loc[:, sub_categories].apply(sum, axis = 1)

  calculated_categories_cols = list(calculated_categories.keys())

  d = d[cols + values + calculated_categories_cols].groupby(cols, as_index=False).sum()

  d = melt(
    d,
    id_vars=cols,
    value_vars=values + calculated_categories_cols,
    var_name='category'
  )

  d['category'] = d['category']\
    .str.extract(r'avg (.*) \/ person \/ day')

  d.loc[:,'medium'] = 'tablet'

  return d

def parse(file):
  # # # loads & parses data
  # # # let's start with the TV dataset
  d_tv = lower_case(concat(
    reduce(concat_files, file['url'][:8], []), ignore_index = True
  ))
  d_tv = parse_tv(d_tv)

  # # # now we do the same for the web data
  d_web = concat(
    reduce(concat_files, file['url'][8:16], []),
    ignore_index = True
  )
  d_web = parse_web(d_web)


  # # # mobile (phone)
  d_mob = concat(
    reduce(concat_files, file['url'][16:24], []),
    ignore_index = True
  )
  d_mob = d_mob[~((d_mob['weighted_social_media'] == 0) & (d_mob['weighted_entertainment'] == 0))]
  d_mob = parse_mob(d_mob)

  # # # mobile (tablet)
  d_tab = concat(
    reduce(concat_files, file['url'][24:], []),
    ignore_index = True
  )
  d_tab = d_tab[~((d_tab['weighted_social_media'] == 0) & (d_tab['weighted_entertainment'] == 0))]
  d_tab = parse_tab(d_tab)

  # # # # and we put those 4 together
  d = concat([d_tv, d_web, d_mob, d_tab], ignore_index=True)

  return d\
    .rename({'activityyear': 'year', 'activitymonth': 'month'}, axis=1)\
    .astype({'year': 'int32', 'month': 'int32'})
