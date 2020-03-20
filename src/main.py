from utils import fullpath 
from fastapi_server import app 
import uvicorn 

if __name__ == '__main__':
  uvicorn.run(app)