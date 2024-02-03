# built-in modules
from os import getenv

# venv modules
from pandas import read_csv

bucket = getenv('bucket')

def load(file):
  return read_csv(f's3://{bucket}/{file}')

def parse(file):
  data = load(file["url"])

  return data
