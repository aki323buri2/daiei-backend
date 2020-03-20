from utils import fullpath 
from fastapi import FastAPI 
import uvicorn 

from models import table_describe 
from models import tran  
from models import hinsyu  

app = FastAPI()

@app.get('/')
def hello():
  return 'hello'

app.include_router(
  table_describe.router, 
  prefix='/describe', 
)

app.include_router(
  tran.router, 
  prefix='/tran', 
)

app.include_router(
  hinsyu.router, 
  prefix='/hinsyu', 
)

if __name__ == '__main__':
  uvicorn.run(app)