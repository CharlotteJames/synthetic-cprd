import os
import sqlite3
import pandas as pd

os.chdir('data/cprd/')
con = sqlite3.connect("cprd.db")

files = [f for f in os.listdir('raw') if '.csv' in f]

for f in files:

    df = pd.read_csv('raw/' + f, dtype=str)
    df.to_sql(f.split('.')[0], con=con, if_exists='replace')

print('database cprd.db built')
