# function to lock colours


# data connection to mysql server

from dash.dependencies import ClientsideFunction
from sqlalchemy import create_engine

import pymysql

import pandas as pd
import numpy as np


# DATA PREP
sqlEngine       = create_engine('mysql+pymysql://root:hoopproj1@127.0.0.1', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

frame = pd.read_sql("SELECT * FROM elections.elections", dbConnection);
pd.set_option('display.expand_frame_repr', False)

dbConnection.close()

gender_state_race = frame[['STATE', 'GENDER', 'RACE']]

 # insert conn.py edf as frame

#Generate New Columns for AGE_GROUP
#change str type to int for age
frame = frame[frame['AGE'] != '#VALUE!']
frame = frame[frame['AGE'] != '#VALU']
frame['AGE'] = frame['AGE'].astype(int)



filtered = gender_state_race[gender_state_race.STATE == 'SELANGOR']
number_ = filtered.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
number_1 = number_.reset_index()
df = pd.DataFrame(data=number_1, columns = ['GENDER', 'RACE', 'STATE'])
racs = df['RACE'].tolist()
print(racs)

# def rac_list(df):


def cols(racs):
    clist = []
    for i in racs:
        if i == 'BPSBH':
            col = '#0077B6'
        elif i ==  'BPSWK':
            col = '#023E8A'
        elif i == 'C':
            col = '#0096C7'
        elif i == 'I':
            col = '#00B48D'
        elif i == 'L':
            col = '#48CAE4'
        elif i == 'M':
            col = '#03045E'
        elif i == 'OA':
            col = '#90E0EF'
        clist.append(col)

    return clist

colors = cols(racs)

print(colors)




