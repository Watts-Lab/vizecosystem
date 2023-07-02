# built-in modules
from math import ceil

# venv modules
from pandas import read_csv, melt

month_range = range(1,13)

def load(f):
  return read_csv(f)

def CREATE_FAKE_DATES(d):
    # THIS IS PROVISIONAL BECAUSE THE DATA DOESNT HAVE DATES
    n_rows = d.shape[0]
    
    total_years = ceil(n_rows / len(month_range))
    
    year_range = range(2016, 2016 + total_years)
    
    add_months = (list(month_range) * total_years)[0:n_rows]
    add_years = sorted(list(year_range) * 12)[0:n_rows]
    
    d['month'] = add_months
    d['year'] = add_years

    return d

def parse_tv(d):
    d = CREATE_FAKE_DATES(d)

    cols = [
        'year',
        'month',
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

    return d

def parse_web(d):
    d = CREATE_FAKE_DATES(d)
    cols = [
        'year',
        'month',
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

    d = melt(
        d,
        id_vars=cols,
        value_vars=values,
        var_name='category'
    )

    d['category'] = d['category']\
        .str.extract(r'avg (.*)[_|\s]mins \/ person \/ day')

    return d

def parse(file):
    # # loads & parses data
    # # let's start with the TV dataset
    d_tv = load(f'~/Desktop/upenn/media-consumption/vizecosystem/{file["url"][0]}')
    d_tv = parse_tv(d_tv)

    # # let's start with the TV dataset
    d_web = load(f'~/Desktop/upenn/media-consumption/vizecosystem/{file["url"][1]}')
    d_web = parse_web(d_web)

    return d_web