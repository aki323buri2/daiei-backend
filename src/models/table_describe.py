from utils import fullpath
from glob import glob 
import pandas as pd 
import json, re, os
from fastapi import APIRouter

import settings 

router = APIRouter()

#####################################
# route
#####################################
@router.get('/tablelist')
async def table_list_route():
  return table_list()

@router.get('/{tablename}')
async def table_describe_route(tablename):
  return table_describe(tablename)

#####################################
# constants
#####################################
CSV_ROOT = settings.CSV_ROOT 
print(CSV_ROOT)
DESCRIPTION_FILTER = '_describe_*_*_*(*).csv'
DESCRIPTION_FILTER_REGEX = r'\[(.+)_(.+)_(.+)\]_\((.+)\)'

def describe_filename_filter(tablename):
  return '_describe_*_{}_*_({}).csv'.format(tablename.upper(), tablename)

#####################################
# get data
#####################################
# get table list 
def table_list():
  # glob files
  dirname = CSV_ROOT
  filter = '{}{}{}'.format(dirname, os.sep, DESCRIPTION_FILTER)
  filenames = glob(filter)
  
  # parse info from filename 
  data = [table_info(fullpath(filename).name) for filename in filenames]

  return data 

# parse info from filename 
def table_info(filename):
  match = re.findall(DESCRIPTION_FILTER_REGEX, filename)
  if len(match) == 0:
    raise Exception('{}: テーブル名情報が取得できません')
  
  id, upper, title, name = match[0]

  return {
    'id': id, 
    'name': name, 
    'upper': upper, 
    'title': title, 
    'filename': filename, 
  }

# load columns descxription by tablename 
def table_describe(tablename):

  df, info = table_describe_dataframe(tablename)

  _dict = dict(zip(
    df['prefix'] + '_' + df['name'], 
    df.to_dict(orient='record')))

  return {
    'info': info, 
    'dict': _dict, 
  }

# description as dataframe
def table_describe_dataframe(tablename):
  dirname = CSV_ROOT
  filter = describe_filename_filter(tablename)
  filter = '{}{}{}'.format(dirname, os.sep, filter)
  filenames = glob(filter)

  if len(filenames) == 0:
    raise Exception('{}: パターンのファイルが見つかりません'.format(filter))

  filename = fullpath(filenames[0])

  info = table_info(filename.name)

  df = pd.read_csv(filename).fillna('')

  return df, info

###############################################
# test code
###############################################
if __name__ == '__main__':
  tablename = 'urikaktrn'
  
  data = table_describe(tablename)

  print(json.dumps(data, ensure_ascii=False, indent=2))

