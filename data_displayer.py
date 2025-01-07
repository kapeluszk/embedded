from db_handler import fetch_measurements, fetch_plant_references
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

app.layout = html.Div([
    dcc.Dropdown(
        id='plant-dropdown',
        options=[
            {'label': 'Tomato', 'value': 'Tomato'},
            {'label': 'Rhubarb', 'value': 'Rhubarb'},
            # Dodaj więcej opcji dla innych roślin
        ],
        value='Tomato'
    ),
    dcc.Graph(id='temperature-graph'),
    dcc.Graph(id='illuminance-graph'),
    dcc.Graph(id='moisture-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('temperature-graph', 'figure'),
    Output('illuminance-graph', 'figure'),
    Output('moisture-graph', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('plant-dropdown', 'value')
)
def update_graphs(n, plant_name):
    measurements = get_measurements()
    df = pd.DataFrame(measurements, columns=['id', 'timestamp', 'temperature', 'illuminance', 'moisture'])

    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        ref_values = fetch_plant_references(cur, plant_name)

    if ref_values is None:
        ref_values = [0, 0, 0]

    temp_fig = px.line(df, x='timestamp', y='temperature', title='Temperature over Time')
    temp_fig.add_scatter(x=df['timestamp'], y=[ref_values[0]]*len(df), mode='lines', name=f'{plant_name} Reference')

    ilu_fig = px.line(df, x='timestamp', y='illuminance', title='Illuminance over Time')
    ilu_fig.add_scatter(x=df['timestamp'], y=[ref_values[1]]*len(df), mode='lines', name=f'{plant_name} Reference')

    moist_fig = px.line(df, x='timestamp', y='moisture', title='Moisture over Time')
    moist_fig.add_scatter(x=df['timestamp'], y=[ref_values[2]]*len(df), mode='lines', name=f'{plant_name} Reference')

    return temp_fig, ilu_fig, moist_fig

def data_display():
    app.run_server(host='0.0.0.0',port=8050,debug=True)