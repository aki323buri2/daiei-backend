from utils import fullpath 
from fastapi import APIRouter 
import pandas as pd 
import settings 
##############################################
# router
##############################################
router = APIRouter()
@router.get('/')
async def urisaki_dataframe_route(buscd='0281'):
  df = urisaki_dataframe(buscd)
  return df.to_dict(orient='record')
##############################################
# constants
##############################################
CSV_ROOT = settings.CSV_ROOT 
URISAKI_CSV = fullpath(CSV_ROOT, 'urisaki.csv')
###############################################
# dataframe
###############################################
def urisaki_dataframe(buscd):
  filename = URISAKI_CSV

  if not buscd is None: 
    name = '{}_{}{}'.format(
      filename.stem, 
      buscd, 
      filename.suffix, 
    )
    filename = filename.parent / name 

  if filename.exists() == False:
    raise Exception('{}が存在しません'.format(filename))

  df = pd.read_csv(filename, low_memory=False, dtype=str).fillna('')

  # 数字をマスク
  df = maskNumbersToDataFrame(df, prefix='AIT')

  return df 

##################################################
# mask numbers
##################################################
def maskNumbers(s):
  s = s.translate(str.maketrans('0123456789', 'X'*10))
  s = s.translate(str.maketrans('０１２３４５６７８９', 'Ｘ'*10))
  return s 

def maskNumbersToDataFrame(df, prefix):
  addrcols = [
    'ADRS1', 
    'ADRS2', 
    'ADRS3', 
    'ADRS4', 
    'ADRS5', 
    'ADRG1', 
    'ADRG2', 
    'ADRG3', 
    'ADRG4', 
    'ADRG5', 
    'ADRD1', 
    'ADRD2', 
    'ADRD3', 
    'ADRD4', 
    'ADRD5', 
  ]
  telncols = [
    'YUBIN', 
    'YUBND', 
    'TELNO',  
    'TELND',  
    'TELNG',  
    'FAXNO', 
  ]
  # プレフィックス付加
  addrcols = ['_'.join([prefix, name]) for name in addrcols]
  telncols = ['_'.join([prefix, name]) for name in telncols]

  def f(x):
    for col in addrcols: 
      s = x[col]
      # 全部マスク
      s = maskNumbers(s)
      x[col] = s

    for col in telncols:
      s = x[col]
      # 後ろ５文字だけマスク
      a = s[:5]
      b = s[5:]
      x[col] = ''.join([a, maskNumbers(b)])

    return x

  df = df.apply(f, axis='columns')

  return df 