from utils import fullpath 
from dateutil.relativedelta import relativedelta 
from dateutil.parser import parse 
from fastapi import APIRouter 
import pandas as pd 
import settings

tablename = 'urikaktrn'
buscd = '0281'
ymd = '2020-02-15'
aitcd = '5292'
denno = '281212720797'

##############################################
# router
##############################################
router = APIRouter()
@router.get('/{tablename}')
def tran_read_dataframe_route(tablename, buscd, ymd, aitcd=None, denno=None):
  df = tran_read_dataframe(tablename, buscd, ymd, aitcd, denno)
  return df.to_dict(orient='record')

@router.get('/{tablename}/summary')
def tran_read_dataframe_summary_route(tablename, buscd, ymd):
  df = tran_read_dataframe(tablename, buscd, ymd)

  # 相手先CD、伝票NOごとの金額集計
  keyCols = ['URI_AITCD', 'URI_DENNO']
  groupby = df.groupby(keyCols)['URI_KINGK']
  size = groupby.size().reset_index().set_index(keyCols).rename(columns={'URI_KINGK': 'KENSU'})
  kin = groupby.sum().reset_index().set_index(keyCols)
  merged = size.merge(kin, on=keyCols).reset_index()

  return merged.to_dict(orient='record')

##############################################
# constants
##############################################
CSV_ROOT = settings.CSV_ROOT 
DATE_COMPARE_FORMAT = '%Y-%m-%d %H:%M:%S'

def tran_read_dataframe(tablename, buscd, ymd, aitcd=None, denno=None):
  
  ymd = parse(ymd)

  filename = tran_create_filename(tablename, buscd, ymd)
  df = pd.read_csv(filename).fillna('')

  df = df[df['URI_SRYMD'] == ymd.strftime(DATE_COMPARE_FORMAT)]

  if not aitcd is None:
    df = df[df['URI_AITCD'] == int(aitcd)]
  
  if not denno is None: 
    df = df[df['URI_DENNO'] == int(denno)]

  return df 


def tran_create_filename(tablaname, buscd, ymd):
  ymd1 = ymd + relativedelta(day=1)
  ymd2 = ymd + relativedelta(day=31)

  filename = '{}_{}_{:%Y-%m-%d}_{:%Y-%m-%d}.csv'.format(tablename, buscd, ymd1, ymd2)

  filename = fullpath(CSV_ROOT, filename)

  if filename.exists() == False:
    raise Exception('{}: ファイルが見つかりません'.format(filename))
  
  return filename 


if __name__ == '__main__':
  df = tran_read_dataframe(tablename, buscd, ymd, aitcd, denno)

  print(df['URI_DENNO'])

  

