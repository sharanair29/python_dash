import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from folium.raster_layers import TileLayer
from numpy import False_, string_, tile
from pandas.core.frame import DataFrame
from pandas.io.formats import style
import plotly.graph_objs as go
import plotly.express as px
from collections import Counter
from branca.utilities import legend_scaler
import folium
import json
import os
import pandas as pd


# data connection to mysql server

from sqlalchemy import create_engine

import pymysql

import pandas as pd
import numpy as np
 

sqlEngine       = create_engine('mysql+pymysql://root:password@127.0.0.1', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

frame = pd.read_sql("SELECT * FROM elections.elections", dbConnection);
pd.set_option('display.expand_frame_repr', False)

dbConnection.close()



 # insert conn.py edf as frame

#Generate New Columns for AGE_GROUP
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


# #Generate Map
# m=folium.Map(location=[3.0738, 101.5183], zoom_start=3)


# tooltip = 'Click For More Info'

# overlay= os.path.join('data', 'over.json')

# folium.GeoJson(overlay, name='states').add_to(m)

# #Create markers
# folium.Marker([3.0738, 101.5183], 
#             popup='<strong>Location One</strong>',
#             tooltip=tooltip).add_to(m)


# Average Age per State
frame['AGE'] = frame['AGE'].astype(int)
age = frame[['STATE', 'AGE']]
ageg = age.groupby(['STATE'])['AGE'].mean().reset_index()


# folium.Choropleth(
#     id = 'map',
#     location=[3.0738, 101.5183], 
#     geo_data=overlay,
#     name='choropleth',
#     data=ageg,
#     columns=['STATE', 'AGE'],
#     key_on='feature.id',
#     fill_color='YlGn',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Age Data'

# ).add_to(m)


# folium.LayerControl().add_to(m)

# m.save('map.html')


# Retrieve counts from MALAYSIA
par_count = frame['PAR'].nunique()
dun_count = frame['DUN'].nunique()
dm_count = frame['DM'].nunique()
locality_count = frame['LOCALITY'].nunique()
state_count = frame['STATE'].nunique()

# #Retrieve States for Drop Down

state_list = frame['STATE'].unique()
par_list = frame['PAR'].unique()
dun_list = frame['DUN'].unique()
dm_list = frame['DM'].unique()
local_list = frame['LOCALITY'].unique()

# #RETRIEVE GENDER COMPOSITION BY RACE

gender_state_race = frame[['STATE', 'GENDER', 'RACE']]
gender_par_race = frame[['STATE','PAR','GENDER', 'RACE']]
gender_dun_race = frame[['STATE','PAR','DUN','GENDER', 'RACE']]
gender_dm_race = frame[['STATE','PAR', 'DUN','DM','GENDER', 'RACE']]
gender_local_race = frame[['STATE', 'PAR', 'DUN', 'DM','LOCALITY', 'GENDER', 'RACE']]

# RETRIEVE AGE AND GENDER

gender_state_age_group = frame[['STATE', 'GENDER', 'AGE_GROUP']]
gender_par_age_group = frame[['STATE','PAR', 'GENDER', 'AGE_GROUP']]
gender_dun_age_group = frame[['STATE','PAR', 'DUN', 'GENDER', 'AGE_GROUP']]
gender_dm_age_group = frame[['STATE', 'PAR', 'DUN', 'DM', 'GENDER', 'AGE_GROUP']]
gender_local_age_group = frame[['STATE', 'PAR', 'DUN', 'DM', 'LOCALITY', 'GENDER', 'AGE_GROUP']]

race_state_agegroup = frame[['STATE', 'RACE', 'AGE_GROUP']]
race_par_agegroup = frame[['STATE','PAR', 'RACE', 'AGE_GROUP']]
race_dun_agegroup = frame[['STATE','PAR', 'DUN', 'RACE', 'AGE_GROUP']]
race_dm_agegroup = frame[['STATE', 'PAR', 'DUN', 'DM', 'RACE', 'AGE_GROUP']]
race_local_agegroup = frame[['STATE', 'PAR', 'DUN', 'DM', 'LOCALITY', 'RACE', 'AGE_GROUP']]
# dash app

app = dash.Dash(__name__, )

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.P('MALAYSIAN ELECTORAL DISTRICTS : DEMOGRAPHICS BY CONSTITUENCIES', style={'margin-bottom': '0px', 'color': 'white','fontSize': 25}),
            ])

        ], className='one-half column', id= 'title'),

        html.Div([
            #html.H6('Last Updated: ',
            #style={'color': 'white'})

        ], className='one-third column', id= 'title1')

    ], id = 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
             html.H6(children='COUNT OF STATES',
             style={'textAlign':'center',
             'color': 'white', 'fontSize':15}),
             html.P(f"{state_count:,.0f}",
             style={'textAlign':'center',
             'color':'white',
             'fontSize':40})
         ], className= 'card_container three columns'),

        html.Div([
            html.H6(children='COUNT OF PAR', 
            style={'textAlign':'center', 
                   'color': 'white', 'fontSize':15}),
            html.P(f"{par_count:,.0f}",
            style={'textAlign':'center', 
            'color': 'white',
            'fontSize':40}),


        ], className= 'card_container three columns'),
    
        html.Div([
            html.H6(children='COUNT OF DUN', 
            style={'textAlign':'center', 
                   'color': 'white', 'fontSize':15}),
            html.P(f"{dun_count:,.0f}",
            style={'textAlign':'center', 
            'color': 'white',
            'fontSize':40}),

         ], className= 'card_container three columns'),

         html.Div([
            html.H6(children='COUNT OF DM', 
            style={'textAlign':'center', 
                   'color': 'white', 'fontSize':15}),
            html.P(f"{dm_count:,.0f}",
            style={'textAlign':'center', 
            'color': 'white',
            'fontSize':40}),

         ], className= 'card_container three columns'),

         html.Div([
            html.H6(children='COUNT OF LOCALITIES', 
            style={'textAlign':'center', 
                   'color': 'white', 'fontSize':15}),
            html.P(f"{locality_count:,.0f}",
            style={'textAlign':'center', 
            'color': 'white',
            'fontSize':40}),

         ], className= 'card_container three columns'),

         html.Div([
             html.P("", style={'color':'white'})
         ], className='create_container_label one column')

    ], className='row flex-display'),

    html.Div([
         html.Div([
            html.P('SELECT STATE:', className='fix_label', style={'color':'white','fontSize':15}),
            dcc.Dropdown(id = 'w_states',
                        multi = False,
                        searchable = True,
                        value='SELANGOR',
                        placeholder='Select States',
                        options= [{'label': c, 'value' : c}
                                  for c in state_list], className='dcc_compon'),
           
         ], className='create_container three columns'),

         html.Div([
            html.P('SELECT PAR:', className='fix_label', style={'color':'white','fontSize':15}),
            dcc.Dropdown(id = 'w_par',
                        multi = False,
                        searchable = True,
                        value='AMPANG',
                        placeholder='Select PAR',
                        options= [{'label': c, 'value' : c}
                                  for c in par_list], className='dcc_compon'),

         ], className='create_container three columns'),
         
         html.Div([
             html.P("SELECT DUN:", className='fix_label', style={'color':'white','fontSize':15}),
             dcc.Dropdown(id = 'w_dun',
                        multi = False,
                        searchable = True,
                        value='BUKIT ANTARABANGSA',
                        placeholder='Select DUN',
                        options= [{'label': c, 'value' : c}
                                  for c in dun_list], className='dcc_compon'),
         ], className='create_container three columns'),

         html.Div([
             html.P("SELECT DM:", className='fix_label', style={'color':'white','fontSize':15}),
             dcc.Dropdown(id = 'w_dm',
                        multi = False,
                        searchable = True,
                        value='TAMAN CAHAYA',
                        placeholder='Select DM',
                        options= [{'label': c, 'value' : c}
                                  for c in dm_list], className='dcc_compon'),
         ], className='create_container three columns'),

         html.Div([
             html.P("SELECT LOCALITY:", className='fix_label', style={'color':'white','fontSize':15}),
             dcc.Dropdown(id = 'w_local',
                        multi = False,
                        searchable = True,
                        value='APT BELA VISTA',
                        placeholder='Select LOCALITY',
                        options= [{'label': c, 'value' : c}
                                  for c in local_list], className='dcc_compon'),
         ], className='create_container three columns'),

         html.Div([
             html.P("", style={'color':'white'})
         ], className='create_container_label one column')

    ], className = 'row flex-display'),

     html.Div([
         html.Div([
             dcc.Graph(id= 'c_gender_state', config = {'displayModeBar':False})
         ], className='create_container three columns'),


         html.Div([
             dcc.Graph(id= 'c_gender_par', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_gender_dun', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_gender_dm', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_gender_local', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             html.P("GENDER X RACE", style={'color':'white'})
         ], className='create_container_label one column')

     ], className = 'row flex-display'),

     html.Div([
         html.Div([
             dcc.Graph(id='age1_state', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id='age1_par', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id='age1_dun', config = {'displayModeBar':False})
         ], className='create_container three columns'),
         
         html.Div([
             dcc.Graph(id='age1_dm', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id='age1_local', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             html.P("RACE X AGE", style={'color':'white'})
         ], className='create_container_label one column')
         
    ], className = 'row flex-display'),

     html.Div([
         html.Div([
             dcc.Graph(id= 'c_race_state', config = {'displayModeBar':False})
         ], className='create_container three columns'),


         html.Div([
             dcc.Graph(id= 'c_race_par', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_race_dun', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_race_dm', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             dcc.Graph(id= 'c_race_local', config = {'displayModeBar':False})
         ], className='create_container three columns'),

         html.Div([
             html.P("AGE X GENDER", style={'color':'white'})
         ], className='create_container_label one column')

     ], className = 'row flex-display'),

     

    html.Div([
        html.Div([
            html.Iframe(
                # id='map', srcDoc=open('','r').read(), width ='100%', height ='600'
            )
        

        ], className = 'create_container twelve columns'),
        html.Div([
             html.P("MAP", style={'color':'white'})
         ], className='create_container_label one column')
    ], className = 'row flex-display')

    

], id = 'mainContainer', style ={'display': 'flex', 'flex-direction': 'column'})

## FUNCTIONS
# colour lock function colors = ['#03045E', '#0077B6', '#023E8A', '#0096C7','#00B48D','#48CAE4', '#90E0EF']

def cols(racs):
    clist = []
    for i in racs:
        if i == 'BPSBH':
            col = '#023E8A'
        elif i ==  'BPSWK':
            col = '#90E0EF'
        elif i == 'C':
            col = '#64dfdf'
        elif i == 'I':
            col = '#00B48D'
        elif i == 'L':
            col = '#0096C7'
        elif i == 'M':
            col = '#03045E'
        elif i == 'OA':
            col = '#80ffdb'
        clist.append(col)
    return clist

# colour by gender

def colsG(genders):
    clist = []
    for i in genders:
        if i == 'FEMALE':
            col = '#2ec4b6'
        elif i ==  'MALE':
            col = '#00004f'
        clist.append(col)
    return clist


# function to retrieve top5 age groups in ascending order 

# for RACE x AGE charts

def top5RA(dfg1_):
    new = dfg1_.groupby('AGE_GROUP')['STATE'].agg(MySum='sum')
    top5 = new.nlargest(5, 'MySum')
    topages = top5.index.tolist()
    dfg1_ = dfg1_[dfg1_['AGE_GROUP'].isin(topages)]
    name_sort = {'0-5': 0,'5-10':1,'11-15':2, '16-20':3, '21-25':4,'26-30':5, '31-35':6,'36-40':7, '41-45':8, '46-50':9, '51-55':10, '56-60':11, '61-65':12, '66-70':13, '71-75':14, '76-80':15, '81-85':16, '86-90':17, '91-95':18, '96-100':19, '100+':20}
    dfg1_['name_sort'] = dfg1_.AGE_GROUP.map(name_sort)
    dfg1_ = dfg1_.sort_values(['name_sort', 'RACE'])

    return dfg1_


# for GENDER X AGE charts

def top5GA(dfg1_):
    new = dfg1_.groupby('AGE_GROUP')['STATE'].agg(MySum='sum')
    top5 = new.nlargest(5, 'MySum')
    topages = top5.index.tolist()
    dfg1_ = dfg1_[dfg1_['AGE_GROUP'].isin(topages)]
    name_sort = {'0-5': 0,'5-10':1,'11-15':2, '16-20':3, '21-25':4,'26-30':5, '31-35':6,'36-40':7, '41-45':8, '46-50':9, '51-55':10, '56-60':11, '61-65':12, '66-70':13, '71-75':14, '76-80':15, '81-85':16, '86-90':17, '91-95':18, '96-100':19, '100+':20}
    dfg1_['name_sort'] = dfg1_.AGE_GROUP.map(name_sort)
    dfg1_ = dfg1_.sort_values(['name_sort', 'GENDER'])

    return dfg1_

## BAR CHARTS PER ROW 

## GENDER X RACE Charts

# STATE GENDER X RACE
@app.callback(Output('c_gender_state','figure'),
Input('w_states','value'))

def update_genderstate(w_states):
     filtered = gender_state_race[gender_state_race.STATE == w_states]
     number_ = filtered.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
     number_1 = number_.reset_index()
     df = pd.DataFrame(data=number_1, columns = ['GENDER', 'RACE', 'STATE'])
     
     female_count_state = len(filtered[filtered['GENDER'] == 'FEMALE'])
     male_count_state = len(filtered[filtered["GENDER"] =='MALE'])

     racs = df['RACE']

     return{
         'data' : [go.Bar(
             x=df.iloc[:,0],
             y=df.iloc[:,2],
             name='Gender and Race Composition',
             marker=dict(color=cols(racs)),
             hoverinfo='text',
             hovertext= 
             '<b>Gender</b>: ' + df['GENDER'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in df['STATE']]+ '<br>'+
             '<b>Race</b>: ' + df['RACE'].astype(str) + '<br>'
              
         )],
         'layout': go.Layout(
             title={'text':'TOTAL: ' + f'{len(filtered)}    ' + 
             'F: ' + f'{female_count_state}    ' + 
             'M: ' + f'{male_count_state}',
             'y':0.93,
             'x':0.5,
             'xanchor':'center',
             'yanchor':'top'},
             titlefont={'color':'black',
             'size':12},
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>GENDER</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
            # plot_bgcolor='#1b2222',
            # paper_bgcolor ='#1b2222'
        
         )
     }

# PAR GENDER X RACE
@app.callback(Output('c_gender_par','figure'),
Input('w_par','value'))

def update_genderpar(w_par):
     filtered2 = gender_par_race[gender_par_race.PAR == w_par]
     number_2 = filtered2.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
     number_3 = number_2.reset_index()
     df2 = pd.DataFrame(data=number_3, columns = ['GENDER', 'RACE', 'STATE'])
     female_count_state2 = len(filtered2[filtered2['GENDER'] == 'FEMALE'])
     male_count_state2 = len(filtered2[filtered2["GENDER"] =='MALE'])
     racs = df2['RACE']

     return{
         'data' : [go.Bar(
             x=df2.iloc[:,0],
             y=df2.iloc[:,2],
             name='Gender and Race Composition',
             marker=dict(color=cols(racs)),
             hoverinfo='text',
             hovertext= 
             '<b>Gender</b>: ' + df2['GENDER'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in df2['STATE']]+ '<br>'+
             '<b>Race</b>: ' + df2['RACE'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             title={'text':'TOTAL: ' + f'{len(filtered2)}    ' + 
             'F: ' + f'{female_count_state2}    ' + 
             'M: ' + f'{male_count_state2}',
             'y':0.93,
             'x':0.5,
             'xanchor':'center',
             'yanchor':'top'},
             titlefont={'color':'black',
             'size':12},
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>GENDER</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }

# DUN GENDER X RACE

@app.callback(Output('c_gender_dun','figure'),
Input('w_dun','value'))

def update_genderdun(w_dun):
     filtered3 = gender_dun_race[gender_dun_race.DUN == w_dun]
     number_4 = filtered3.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
     number_5 = number_4.reset_index()
     df3 = pd.DataFrame(data=number_5, columns = ['GENDER', 'RACE', 'STATE'])
     female_count_state3 = len(filtered3[filtered3['GENDER'] == 'FEMALE'])
     male_count_state3 = len(filtered3[filtered3["GENDER"] =='MALE'])
     racs = df3['RACE']

     return{
         'data' : [go.Bar(
             x=df3.iloc[:,0],
             y=df3.iloc[:,2],
             name='Gender and Race Composition',
             marker=dict(color=cols(racs)),
             hoverinfo='text',
             hovertext= 
             '<b>Gender</b>: ' + df3['GENDER'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in df3['STATE']]+ '<br>'+
             '<b>Race</b>: ' + df3['RACE'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             title={'text':'TOTAL: ' + f'{len(filtered3)}    ' + 
             'F: ' + f'{female_count_state3}    ' + 
             'M: ' + f'{male_count_state3}',
             'y':0.93,
             'x':0.5,
             'xanchor':'center',
             'yanchor':'top'},
             titlefont={'color':'black',
             'size':12},
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>GENDER</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }

# DM GENDER X RACE

@app.callback(Output('c_gender_dm','figure'),
Input('w_dm','value'))

def update_genderdm(w_dm):
     filtered4 = gender_dm_race[gender_dm_race.DM == w_dm]
     number_6 = filtered4.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
     number_7 = number_6.reset_index()
     df4 = pd.DataFrame(data=number_7, columns = ['GENDER', 'RACE', 'STATE'])
     female_count_state4 = len(filtered4[filtered4['GENDER'] == 'FEMALE'])
     male_count_state4 = len(filtered4[filtered4["GENDER"] =='MALE'])
     racs = df4['RACE']

     return{
         'data' : [go.Bar(
             x=df4.iloc[:,0],
             y=df4.iloc[:,2],
             name='Gender and Race Composition',
             marker=dict(color=cols(racs)),
             hoverinfo='text',
              hovertext= 
             '<b>Gender</b>: ' + df4['GENDER'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in df4['STATE']]+ '<br>'+
             '<b>Race</b>: ' + df4['RACE'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             title={'text':'TOTAL: ' + f'{len(filtered4)}    ' + 
             'F: ' + f'{female_count_state4}    ' + 
             'M: ' + f'{male_count_state4}',
             'y':0.93,
             'x':0.5,
             'xanchor':'center',
             'yanchor':'top'},
             titlefont={'color':'black',
             'size':12},
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>GENDER</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }

# LOCAL GENDER X RACE

@app.callback(Output('c_gender_local','figure'),
Input('w_local','value'))

def update_genderdm(w_local):
     filtered5 = gender_local_race[gender_local_race.LOCALITY == w_local]
     number_8 = filtered5.groupby(['GENDER','RACE'], sort=True, group_keys=True).count()
     number_9 = number_8.reset_index()
     df5 = pd.DataFrame(data=number_9, columns = ['GENDER', 'RACE', 'STATE'])
     female_count_state5 = len(filtered5[filtered5['GENDER'] == 'FEMALE'])
     male_count_state5 = len(filtered5[filtered5["GENDER"] =='MALE'])
     racs = df5['RACE']

     return{
         'data' : [go.Bar(
             x=df5.iloc[:,0],
             y=df5.iloc[:,2],
             name='Gender and Race Composition',
             marker=dict(color=cols(racs)),
             hoverinfo='text',
              hovertext= 
             '<b>Gender</b>: ' + df5['GENDER'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in df5['STATE']]+ '<br>'+
             '<b>Race</b>: ' + df5['RACE'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             title={'text':'TOTAL: ' + f'{len(filtered5)}    ' + 
             'F: ' + f'{female_count_state5}    ' + 
             'M: ' + f'{male_count_state5}',
             'y':0.93,
             'x':0.5,
             'xanchor':'center',
             'yanchor':'top'},
             titlefont={'color':'black',
             'size':12},
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>GENDER</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }




## race x age

# STATE RACE X AGE
@app.callback(Output('age1_state','figure'),
Input('w_states','value'))

def age_state(w_states):
    filter = race_state_agegroup[race_state_agegroup.STATE == w_states]
    g1 = filter.groupby(['RACE','AGE_GROUP'], sort=True, group_keys=True).count()
    dfg1 = g1.reset_index()
    dfg1_= pd.DataFrame(data=dfg1, columns=['RACE','AGE_GROUP', 'STATE'])
    tops = top5RA(dfg1_)
    racs = tops['RACE']
 

    return{
        'data' : [go.Bar(
            x=tops.iloc[:,1],
            y=tops.iloc[:,2],
            name='Age Group Count',
            marker=dict(color=cols(racs)),
            hoverinfo='text',
            hovertext= 
            '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
            '<b>Count </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>' + 
            '<b>Race </b>: ' + tops['RACE'].astype(str)
            
        )],
        'layout': go.Layout(
            titlefont={'color':'black',
            'size':10},
            hovermode='closest',
            legend={'orientation':'h',
            'xanchor':'center','x': 0.5, 'y':-0.7},
            xaxis = dict(title='<b>AGE GROUP</b>',
                color='black',
                showline = False,
                showgrid=False),
            yaxis= dict(title='<b>COUNT</b>',
                color='black',
                showline = False,
                showgrid=False)
        )
    }

# PAR RACE X AGE
@app.callback(Output('age1_par','figure'),
Input('w_par','value'))

def age_state(w_par):
    filter = race_par_agegroup[race_par_agegroup.PAR == w_par]
    g1 = filter.groupby(['RACE','AGE_GROUP'], sort=True, group_keys=True).count()
    dfg1 = g1.reset_index()
    dfg1_= pd.DataFrame(data=dfg1, columns=['RACE','AGE_GROUP', 'STATE'])
    tops = top5RA(dfg1_)
    racs = tops['RACE']
    
    

    return{
        'data' : [go.Bar(
            x=tops.iloc[:,1],
            y=tops.iloc[:,2],
            name='Age Group Count',
            marker=dict(color=cols(racs)),
            hoverinfo='text',
            hovertext= 
            '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
            '<b>Count </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>' +
            '<b>Race </b>: ' + tops['RACE'].astype(str)
            
        )],
        'layout': go.Layout(
            titlefont={'color':'black',
            'size':10},
            hovermode='closest',
            legend={'orientation':'h',
            'xanchor':'center','x': 0.5, 'y':-0.7},
            xaxis = dict(title='<b>AGE GROUP</b>',
                color='black',
                showline = False,
                showgrid=False),
            yaxis= dict(title='<b>COUNT</b>',
                color='black',
                showline = False,
                showgrid=False)
        )
    }

# DUN RACE X AGE
@app.callback(Output('age1_dun','figure'),
Input('w_dun','value'))

def age_state(w_dun):
    filter = race_dun_agegroup[race_dun_agegroup.DUN == w_dun]
    g1 = filter.groupby(['RACE','AGE_GROUP'], sort=True, group_keys=True).count()
    dfg1 = g1.reset_index()
    dfg1_= pd.DataFrame(data=dfg1, columns=['RACE','AGE_GROUP', 'STATE'])
    tops = top5RA(dfg1_)
    racs = tops['RACE']

    return{
        'data' : [go.Bar(
            x=tops.iloc[:,1],
            y=tops.iloc[:,2],
            name='Age Group Count',
            marker=dict(color=cols(racs)),
            hoverinfo='text',
            hovertext= 
            '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
            '<b>Count </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
            '<b>Race </b>: ' + tops['RACE'].astype(str)
            
        )],
        'layout': go.Layout(
            titlefont={'color':'black',
            'size':10},
            hovermode='closest',
            legend={'orientation':'h',
            'xanchor':'center','x': 0.5, 'y':-0.7},
            xaxis = dict(title='<b>AGE GROUP</b>',
                color='black',
                showline = False,
                showgrid=False),
            yaxis= dict(title='<b>COUNT</b>',
                color='black',
                showline = False,
                showgrid=False)
        )
    }

# DM RACE X AGE
@app.callback(Output('age1_dm','figure'),
Input('w_dm','value'))

def age_state(w_dm):
    filter = race_dm_agegroup[race_dm_agegroup.DM == w_dm]
    g1 = filter.groupby(['RACE', 'AGE_GROUP'], sort=True, group_keys=True).count()
    dfg1 = g1.reset_index()
    dfg1_= pd.DataFrame(data=dfg1, columns=['RACE', 'AGE_GROUP', 'STATE'])
    tops = top5RA(dfg1_)
    racs = tops['RACE']

    return{
        'data' : [go.Bar(
            x=tops.iloc[:,1],
            y=tops.iloc[:,2],
            name='Age Group Count',
            marker=dict(color=cols(racs)),
            hoverinfo='text',
            hovertext= 
            '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
            '<b>Count </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
            '<b>Race </b>: ' + tops['RACE'].astype(str)
            
        )],
        'layout': go.Layout(
            titlefont={'color':'black',
            'size':10},
            hovermode='closest',
            legend={'orientation':'h',
            'xanchor':'center','x': 0.5, 'y':-0.7},
            xaxis = dict(title='<b>AGE GROUP</b>',
                color='black',
                showline = False,
                showgrid=False),
            yaxis= dict(title='<b>COUNT</b>',
                color='black',
                showline = False,
                showgrid=False)
        )
    }

# LOCAL RACE X AGE
@app.callback(Output('age1_local','figure'),
Input('w_local','value'))

def age_state(w_local):
    filter = race_local_agegroup[race_local_agegroup.LOCALITY == w_local]
    g1 = filter.groupby(['RACE','AGE_GROUP'], sort=True, group_keys=True).count()
    dfg1 = g1.reset_index()
    dfg1_= pd.DataFrame(data=dfg1, columns=['RACE','AGE_GROUP', 'STATE'])
    tops = top5RA(dfg1_)
    racs = tops['RACE']
    

    return{
        'data' : [go.Bar(
            x=tops.iloc[:,1],
            y=tops.iloc[:,2],
            name='Age Group Count',
            marker=dict(color=cols(racs)),
            hoverinfo='text',
            hovertext= 
            '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
            '<b>Count </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
            '<b>Race </b>: ' + tops['RACE'].astype(str)
            
        )],
        'layout': go.Layout(
            titlefont={'color':'black',
            'size':10},
            hovermode='closest',
            legend={'orientation':'h',
            'xanchor':'center','x': 0.5, 'y':-0.7},
            xaxis = dict(title='<b>AGE GROUP</b>',
                color='black',
                showline = False,
                showgrid=False),
                
            yaxis= dict(title='<b>COUNT</b>',
                color='black',
                showline = False,
                showgrid=False),
        )
    }


## age x gender

#STATE AGE X GENDER

@app.callback(Output('c_race_state','figure'),
Input('w_states','value'))

def update_racestate(w_states):
     filtered = gender_state_age_group[gender_state_age_group.STATE == w_states]
     number_ = filtered.groupby(['GENDER','AGE_GROUP'], sort=True, group_keys=True).count()
     number_1 = number_.reset_index()
     df = pd.DataFrame(data=number_1, columns = ['GENDER', 'AGE_GROUP', 'STATE'])
     tops = top5GA(df)
     gen = tops['GENDER']
     
    

     return{
         'data' : [go.Bar(
             x=tops.iloc[:,1],
             y=tops.iloc[:,2],
             name='Gender and Age Composition',
             marker=dict(color=colsG(gen)),
             hoverinfo='text',
              hovertext= 
             '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
             '<b>Gender</b>: ' + tops['GENDER'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>AGE GROUP</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }

# PAR AGE X GENDER

@app.callback(Output('c_race_par','figure'),
Input('w_par','value'))

def update_racepar(w_par):
     filtered2 = gender_par_age_group[gender_par_age_group.PAR == w_par]
     number_2 = filtered2.groupby(['GENDER','AGE_GROUP'], sort=True, group_keys=True).count()
     number_3 = number_2.reset_index()
     df = pd.DataFrame(data=number_3, columns = ['GENDER', 'AGE_GROUP', 'STATE'])
     tops = top5GA(df)
     gen = tops['GENDER']
     
    

     return{
         'data' : [go.Bar(
             x=tops.iloc[:,1],
             y=tops.iloc[:,2],
             name='Gender and Age Composition',
             marker=dict(color=colsG(gen)),
             hoverinfo='text',
              hovertext= 
             '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
             '<b>Gender</b>: ' + tops['GENDER'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>AGE GROUP</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }


# DUN AGE X GENDER

@app.callback(Output('c_race_dun','figure'),
Input('w_dun','value'))

def update_racedun(w_dun):
     filtered3 = gender_dun_age_group[gender_dun_age_group.DUN == w_dun]
     number_4 = filtered3.groupby(['GENDER','AGE_GROUP'], sort=True, group_keys=True).count()
     number_5 = number_4.reset_index()
     df = pd.DataFrame(data=number_5, columns = ['GENDER', 'AGE_GROUP', 'STATE'])
     tops = top5GA(df)
     gen = tops['GENDER']

     return{
         'data' : [go.Bar(
             x=tops.iloc[:,1],
             y=tops.iloc[:,2],
             name='Gender and Age Composition',
             marker=dict(color=colsG(gen)),
             hoverinfo='text',
              hovertext= 
             '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
             '<b>Gender</b>: ' + tops['GENDER'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>AGE GROUP</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }



# DM AGE X GENDER

@app.callback(Output('c_race_dm','figure'),
Input('w_dm','value'))

def update_racedun(w_dm):
     filtered4 = gender_dm_age_group[gender_dm_age_group.DM == w_dm]
     number_6 = filtered4.groupby(['GENDER','AGE_GROUP'], sort=True, group_keys=True).count()
     number_7 = number_6.reset_index()
     df = pd.DataFrame(data=number_7, columns = ['GENDER', 'AGE_GROUP', 'STATE'])
     tops = top5GA(df)
     gen = tops['GENDER']
     

     return{
         'data' : [go.Bar(
             x=tops.iloc[:,1],
             y=tops.iloc[:,2],
             name='Gender and Age Composition',
             marker=dict(color=colsG(gen)),
             hoverinfo='text',
              hovertext= 
             '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
             '<b>Gender</b>: ' + tops['GENDER'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>AGE GROUP</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }


# LOCAL AGE X GENDER
@app.callback(Output('c_race_local','figure'),
Input('w_local','value'))

def update_racedun(w_local):
     filtered5 = gender_local_age_group[gender_local_age_group.LOCALITY == w_local]
     number_8 = filtered5.groupby(['GENDER','AGE_GROUP'], sort=True, group_keys=True).count()
     number_9 = number_8.reset_index()
     df = pd.DataFrame(data=number_9, columns = ['GENDER', 'AGE_GROUP', 'STATE'])
     tops = top5GA(df)
     gen = tops['GENDER']
     

     return{
         'data' : [go.Bar(
             x=tops.iloc[:,1],
             y=tops.iloc[:,2],
             name='Gender and Age Composition',
             marker=dict(color=colsG(gen)),
             hoverinfo='text',
              hovertext= 
             '<b>Age</b>: ' + tops['AGE_GROUP'].astype(str) + '<br>' +
             '<b>Count: </b>: ' + [f'{x:,.0f}' for x in tops['STATE']]+ '<br>'+
             '<b>Gender</b>: ' + tops['GENDER'].astype(str) + '<br>'
         )],
         'layout': go.Layout(
             hovermode='closest',
             legend={'orientation':'h',
             'xanchor':'center','x': 0.5, 'y':-0.7},
             xaxis = dict(title='<b>AGE GROUP</b>',
                    color='black',
                    showline = False,
                    showgrid=False),
             yaxis= dict(title='<b>COUNT</b>',
                    color='black',
                    showline = False,
                    showgrid=False)
         )
     }

if __name__ == '__main__':
    app.run_server(debug=True)


   

