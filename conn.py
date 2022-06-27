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
#change str type to int for age
frame = frame[frame['AGE'] != '#VALUE!']
frame = frame[frame['AGE'] != '#VALU']
frame['AGE'] = frame['AGE'].astype(int)
# create a list of our conditions
conditions = [
    (frame['AGE'] <= 5),
    (frame['AGE'] > 5) & (frame['AGE'] <= 10),
    (frame['AGE'] > 10) & (frame['AGE'] <= 15),
    (frame['AGE'] > 15) & (frame['AGE'] <= 20),
    (frame['AGE'] > 20) & (frame['AGE'] <= 25),
    (frame['AGE'] > 25) & (frame['AGE'] <= 30),
    (frame['AGE'] > 30) & (frame['AGE'] <= 35),
    (frame['AGE'] > 35) & (frame['AGE'] <= 40),
    (frame['AGE'] > 40) & (frame['AGE'] <= 45),
    (frame['AGE'] > 45) & (frame['AGE'] <= 50),
    (frame['AGE'] > 50) & (frame['AGE'] <= 55),
    (frame['AGE'] > 55) & (frame['AGE'] <= 60),
    (frame['AGE'] > 60) & (frame['AGE'] <= 65),
    (frame['AGE'] > 65) & (frame['AGE'] <= 70),
    (frame['AGE'] > 70) & (frame['AGE'] <= 75),
    (frame['AGE'] > 75) & (frame['AGE'] <= 80),
    (frame['AGE'] > 80) & (frame['AGE'] <= 85),
    (frame['AGE'] > 85) & (frame['AGE'] <= 90),
    (frame['AGE'] > 90) & (frame['AGE'] <= 95),
    (frame['AGE'] > 95) & (frame['AGE'] <= 100),
    (frame['AGE'] > 100)
    

    
    ]

# create a list of the values we want to assign for each condition
values = ['0-5','5-10','11-15', '16-20', '21-25','26-30', '31-35','36-40', '41-45', '46-50', '51-55', '56-60', '61-65', '66-70', '71-75', '76-80', '81-85', '86-90', '91-95', '96-100', '100+']

# create a new column and use np.select to assign values to it using our lists as arguments
frame['AGE_GROUP'] = np.select(conditions, values)

def top5(dfg1_):
    new = dfg1_.groupby('AGE_GROUP')['STATE'].agg(MySum='sum')
    top5 = new.nlargest(5, 'MySum')
    topages = top5.index.tolist()
    dfg1_ = dfg1_[dfg1_['AGE_GROUP'].isin(topages)]
    name_sort = {'0-5': 0,'5-10':1,'11-15':2, '16-20':3, '21-25':4,'26-30':5, '31-35':6,'36-40':7, '41-45':8, '46-50':9, '51-55':10, '56-60':11, '61-65':12, '66-70':13, '71-75':14, '76-80':15, '81-85':16, '86-90':17, '91-95':18, '96-100':19, '100+':20}
    dfg1_['name_sort'] = dfg1_.AGE_GROUP.map(name_sort)
    dfg1_ = dfg1_.sort_values(['name_sort'])

    return dfg1_


race_local_agegroup = frame[['STATE', 'PAR', 'DUN', 'DM', 'LOCALITY', 'RACE', 'AGE_GROUP']]

filter = race_local_agegroup[race_local_agegroup.LOCALITY == 'APT BELA VISTA']
g1 = filter.groupby(['RACE','AGE_GROUP'], sort=True, group_keys=True).count()
dfg1 = g1.reset_index()
dfg1_= pd.DataFrame(data=dfg1, columns=['RACE','AGE_GROUP', 'STATE'])
tops = top5(dfg1_)

print(tops)