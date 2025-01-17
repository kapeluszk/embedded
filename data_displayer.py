from db_handler import fetch_measurements, fetch_plant_references, fetch_target_moisture, update_target_moisture
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.io as pio
import pandas as pd
import sqlite3
import dash
import time

app = dash.Dash(__name__)

pio.templates.default = 'plotly_dark'

def get_measurements():
    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        measurements = fetch_measurements(cur, 7)
    return measurements

def get_target_moisture():
    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        target_moisture = fetch_target_moisture(cur)
    return target_moisture[0] if target_moisture else 0

app.layout = html.Div(className='container', children=[
    html.H1('Plant Monitoring Dashboard'),
    html.Div(className='dropdown-container', children=[
        html.Label('Select Plant:', className='input-label'),
        dcc.Dropdown(
            id='plant-dropdown',
            options=[
                {'label': 'Tomato', 'value': 'Tomato'},
                {'label': 'Rhubarb', 'value': 'Rhubarb'},
                # Dodaj więcej opcji dla innych roślin
            ],
            value='Tomato',
            className='dccDropdown'
        ),
    ]),
    html.Div(className='input-container', children=[
        html.Label('Target Moisture:', className='input-label'),
        dcc.Input(
            id='target-moisture-input',
            type='number',
            min=0,
            max=100,
            value=get_target_moisture(),
            className='dccInput'
        ),
    ]),
    dcc.Graph(id='temperature-graph', className='dccGraph'),
    dcc.Graph(id='illuminance-graph', className='dccGraph'),
    dcc.Graph(id='moisture-graph', className='dccGraph'),
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
    Input('plant-dropdown', 'value'),
    Input('target-moisture-input', 'value')
)
def update_graphs(n, plant_name, target_moisture):
    measurements = get_measurements()
    df = pd.DataFrame(measurements, columns=['id', 'timestamp', 'temperature', 'illuminance', 'moisture'])

    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        ref_values = fetch_plant_references(cur, plant_name)
        update_target_moisture(conn, cur, target_moisture)
        target_moisture_value = fetch_target_moisture(cur)[0]

    if ref_values is None:
        ref_values = [0, 0, 0]

    temp_fig = px.line(df, x='timestamp', y='temperature', title='Temperature over Time', labels={'temperature': 'Temperature'})
    temp_fig.add_scatter(x=df['timestamp'], y=df['temperature'], mode='lines', name='Temperature')
    temp_fig.add_scatter(x=df['timestamp'], y=[ref_values[0]] * len(df), mode='lines', name=f'{plant_name} Reference')

    ilu_fig = px.line(df, x='timestamp', y='illuminance', title='Illuminance over Time', labels={'illuminance': 'Illuminance'})
    ilu_fig.add_scatter(x=df['timestamp'], y=df['illuminance'], mode='lines', name='Illuminance')
    ilu_fig.add_scatter(x=df['timestamp'], y=[ref_values[1]] * len(df), mode='lines', name=f'{plant_name} Reference')

    moist_fig = px.line(df, x='timestamp', y='moisture', title='Moisture over Time', labels={'moisture': 'Moisture'})
    moist_fig.add_scatter(x=df['timestamp'], y=df['moisture'], mode='lines', name='Moisture')
    moist_fig.add_scatter(x=df['timestamp'], y=[ref_values[2]] * len(df), mode='lines', name=f'{plant_name} Reference')
    moist_fig.add_scatter(x=df['timestamp'], y=[target_moisture_value] * len(df), mode='lines', name='Target Moisture')
    
    return temp_fig, ilu_fig, moist_fig

def data_display():
    app.run_server(host='0.0.0.0', port=8050, debug=True)