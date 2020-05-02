from utils import fullpath 
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 

from models import (
  table_describe, 
  tran, 
  hinsyu, 
  urisaki, 
  kaisaki, 
  gzaikozan, 
  urisaki2, 
) 

app = FastAPI()

app.add_middleware(
  CORSMiddleware, 
  allow_origins=['*'], 
  allow_credentials=True, 
  allow_methods=['*'], 
  allow_headers=['*'], 
)

app.include_router(urisaki2.router, prefix='/urisaki2')
app.include_router(gzaikozan.router, prefix='/gzaikozan')

app.include_router(urisaki.router, prefix='/urisaki')
app.include_router(tran.router, prefix='/tran')
app.include_router(table_describe.router, prefix='/describe')
app.include_router(hinsyu.router, prefix='/hinsyu')
app.include_router(kaisaki.router, prefix='/kaisaki')

if __name__ == '__main__':
  uvicorn.run(app)