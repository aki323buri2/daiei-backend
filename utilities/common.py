# %%
import pandas as pd 
import csv 
from functools import reduce 
from pathlib import Path 

def fullpath(*path):
  root = Path(".")
  full = reduce(lambda a, b: Path(a) / Path(b), path, root)
  return full.resolve().absolute()
def ensure_dir(*path):
  dirname = fullpath(*path)
  dirname.mkdir(exist_ok=True, parents=True)
  return dirname 
class dotdict(dict):
  def __setattr__(self, name, value): 
    self[name] = value 
  def __getattr__(self, name):
    return self[name]
  def to_dict(self):
    return dict(self)
def load_csv(filename, encoding="utf-8_sig", dtype=str, **kargs):
  return pd.read_csv(filename, encoding=encoding, dtype=dtype, **kargs).fillna("")
def save_csv(df, filename, encoding="utf-8_sig", index=False, quoting=csv.QUOTE_ALL, **kargs):
  filename = fullpath(filename)
  df.to_csv(filename, encoding=encoding, index=index, quoting=quoting, **kargs)
  return filename



