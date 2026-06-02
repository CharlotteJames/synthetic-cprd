import os
import sqlite3
import pandas as pd

os.chdir('data/hes_ae/')
con = sqlite3.connect("hes_ae.db")

files = [f for f in os.listdir('raw') if '.csv' in f]

for f in files:

    df = pd.read_csv('raw/' + f, dtype=str)
    df.to_sql(f.split('.')[0], con=con, if_exists='replace')

print('database hes_ae.db built')
