import pandas as pd
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import sqlite3 as sql
from dash import html, Dash, dcc, Input, Output
from flask  import Flask
import dash_bootstrap_components as dbc

from sklearn.linear_model import LinearRegression
 

import os


    
'''Exploratory Data Analysis'''

con = sql.connect("fitbit.db")
cur = con.cursor()

full_info_activity = """
SELECT *,
	STRFTIME('%d',ActivityDate) day,
	STRFTIME('%m',ActivityDate) month,
	STRFTIME('%Y',ActivityDate) year,
	STRFTIME('%w',ActivityDate) dow
FROM dailyActivity_merged;
"""
full_dailyActivity_df = pd.read_sql(full_info_activity, con)

# join daily activity data and sleep data
join_query = """
SELECT
	A.Id,
	A.ActivityDate,
	A.SedentaryMinutes,
	A.LightlyActiveMinutes,
	S.TotalMinutesAsleep
FROM
	dailyActivity_merged A
INNER JOIN sleepDay_merged S
ON
	A.Id = S.Id AND
    A.ActivityDate = S.SleepDay;
"""
activity_sleep_df = pd.read_sql(join_query, con)

dailyActivity_df = pd.read_sql(f'SELECT * FROM dailyActivity_merged', con)


# fit a regression line to totalsteps and calories
X = full_dailyActivity_df['TotalSteps'].values.reshape((-1, 1))
y = full_dailyActivity_df['Calories'].values

figure5 = sns.regplot(X, y, ci=None);


''' Dash Application '''
server = Flask(__name__)

app = Dash(name=__name__, server=server,     external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

figure1 = px.scatter(data_frame= dailyActivity_df, x="VeryActiveMinutes",  y = 'VeryActiveDistance', trendline="ols")
figure2 = px.scatter(data_frame= dailyActivity_df, x = 'FairlyActiveMinutes', y = 'ModeratelyActiveDistance', trendline="ols")
figure3 = px.scatter(data_frame= dailyActivity_df,  x = 'LightlyActiveMinutes', y = 'LightActiveDistance', trendline="ols")
figure4 = px.scatter(data_frame= dailyActivity_df, x = 'SedentaryMinutes', y = 'SedentaryActiveDistance', trendline="ols")





app.layout = html.Div(
    [   
        html.H1("Smartwatch Analysis Dashboard", className="flex-d flex-row"),
        html.Div([
            dcc.Graph(id="graph1", figure=figure1, style={"width": "50%"}), 
            dcc.Graph(id="graph2", figure=figure2, style={"width": "50%"}), 
            dcc.Graph(id="graph3", figure=figure3, style={"width": "50%"}), 
            dcc.Graph(id="graph4", figure=figure4, style={"width": "50%"}), 
                 ],className="d-flex flex-row" ),
        html.P ("Applying Linear Regression to TotalSteps and Calories"),
        dcc.Graph(fig=figure5)
    ]
    )



    




app.run_server(debug=True)
