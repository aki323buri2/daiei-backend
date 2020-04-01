from utils import fullpath 
from fastapi import APIRouter 
import pandas as pd 
import settings 
from models.urisaki import maskNumbersToDataFrame
###############################################
# router
###############################################
router = APIRouter()
@router.get('/')
async def kaisaki_dataframe_route(buscd='0281'):
  df = kaisaki_dataframe(buscd)
  return df.to_dict(orient='record')
###############################################
# constants
###############################################
CSV_ROOT = settings.CSV_ROOT 
KAISAKI_CSV = fullpath(CSV_ROOT, 'kaisaki.csv')
###############################################
# dataframe
###############################################
def kaisaki_dataframe(buscd):
  filename = KAISAKI_CSV 

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