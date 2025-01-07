from db_handler import fetch_measurements
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlite3
import time



app = Dash()

def get_measurements():
    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        measurements = fetch_measurements(cur, 7)
    return measurements

@app.callback(
    Output('temperature-graph', 'figure'),
    Output('illuminance-graph', 'figure'),
    Output('moisture-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(n):
    measurements = get_measurements()
    df = pd.DataFrame(measurements, columns=['id','timestamp', 'temperature', 'illuminance', 'moisture'])

    temp_fig = px.line(df, x='timestamp', y='temperature', title='Temperature over Time')
    ilu_fig = px.line(df, x='timestamp', y='illuminance', title='Illuminance over Time')
    moist_fig = px.line(df, x='timestamp', y='moisture', title='Moisture over Time')

    return temp_fig, ilu_fig, moist_fig

app.layout = html.Div([
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='illuminance-graph'),
    dcc.Graph(id='moisture-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds
        n_intervals=0
    )
])

def data_display():
    app.run_server(host='0.0.0.0',port=8050,debug=True)