from utils import fullpath 
from dotenv import load_dotenv 
import os 
load_dotenv(dotenv_path=fullpath('../.env'))

CSV_ROOT = fullpath('..', os.getenv('CSV_ROOT'))