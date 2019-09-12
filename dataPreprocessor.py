import pandas as pd 
import numpy as np 
import re

moviesDb = pd.read_csv('imdbTop50From2000To2019.csv',index_col='Id')
moviesDb['ReleaseYear'] = moviesDb['ReleaseYear'].apply(lambda x : int(re.findall(r'\(([0-9].*)\)',x)[0]))