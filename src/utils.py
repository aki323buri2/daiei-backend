from pathlib import Path 
from functools import reduce 
import sys 

def fullpath(*path):
  filename = Path(__file__).parent

  relpath = filename / reduce(lambda a, b: Path(a) / Path(b), path)

  return relpath.resolve().absolute()

root = fullpath('.')

if not str(root) in sys.path:
  sys.path.append(str(root))