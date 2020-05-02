from utils import fullpath 
from fastapi import APIRouter 
import pandas as pd 
import settings 

router = APIRouter()

@router.get('/')
async def index():
  df = dataframe()
  return df.to_dict(orient='records')

def dataframe():
  CSV_ROOT = settings.CSV_ROOT 
  filename = fullpath(CSV_ROOT, 'AITSAKMST_U.csv')

  df = pd.read_csv(filename, low_memory=False, dtype=str).fillna('')

  return df 