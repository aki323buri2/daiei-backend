from utils import fullpath 
from fastapi import APIRouter 
import settings 
import pandas as pd 

router = APIRouter()

@router.get('/')
async def index():
  df = dataframe()
  return df.to_dict(orient='records')

def dataframe():
  CSV_ROOT = settings.CSV_ROOT 
  filename = fullpath(CSV_ROOT, 'GZAIKOZAN.csv')

  df = pd.read_csv(filename, low_memory=False).fillna('')

  return df 