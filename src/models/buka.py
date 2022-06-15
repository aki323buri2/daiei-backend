from utils import fullpath 
from fastapi import APIRouter 
import pandas as pd 
import settings 
#########################################
# router
#########################################
router = APIRouter()
@router.get('/')
async def buka_dataframe_route(offset=0, chunk=1000):
  df = buka_dataframe(offset, chunk)
  return df.to_dict(orient='record')

#########################################
# constants
#########################################
CSV_ROOT = settings.CSV_ROOT 
BUKA_CSV = fullpath(CSV_ROOT, 'buka.csv')

def buka_dataframe(offset, chunk):
  filename = BUKA_CSV 
  offset = int(offset)
  chunk = int(chunk)
  df = pd.read_csv(filename, low_memory=False).fillna('')
  df = df[offset:offset + chunk]
  return df 
