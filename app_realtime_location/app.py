#%%


import logging
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine, text

#%%
#Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(funcName)s :: %(message)s",
)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

#%%
# Connect to PostgreSQL database
DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', "postgresql")
DATABASE_ROOT_PASSWORD = os.environ.get('POSTGRES_PASSWORD', "password")
DATABASE_NAME = os.environ.get('POSTGRES_DB', "postgres")
DATABASE_USER = os.environ.get('POSTGRES_USER', "admin")
DATABASE_HOST = os.environ.get('POSTGRES_HOST', "localhost")
DATABASE_PORT = os.environ.get('POSTGRES_PORT', "5433")
logging.info("Imported environmental variables")

#%%

DATABASE_URL = f'{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_ROOT_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
conn = create_engine(DATABASE_URL)
logging.info("Connected to database")

#%%
schema = "public"
table = "latest_locations"
query = f"SELECT * from {schema}.{table};"

#%%
try: 
    with conn.connect() as connection:

        df = pd.read_sql_query(con=connection, sql=query)

        df['measurement_time'] = pd.to_datetime(df['measurement_time'])  # Ensure measurement_time is datetime
        vehicles = list(df['vehicle_id'].unique())
        print(vehicles)
except:
    logging.error(f"Could not query table {table}")

#%%

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

vehicle_dropdown = dcc.Dropdown(
    id="vehicle-dropdown",
    options=[{"label": f"Vehicle {vehicle}", "value": vehicle} for vehicle in vehicles] +
             [{"label": "Select All", "value": "SELECT_ALL"},
              {"label": "Clear All", "value": "CLEAR_ALL"}],
    value=[str(vehicle) for vehicle in vehicles[:-1]],  # Pre-select vehicles except the last
    multi=True,
    clearable=True,
    placeholder="Select a vehicle here",
)

app.layout = html.Div([
    dbc.Container([
        html.H2("Vehicle Last Known Locations"),
        dbc.Row([dbc.Col(vehicle_dropdown, lg=10)]),
        dbc.Row([dbc.Col(dcc.Graph(id="vehicle-map"), lg=10)]),
    ], fluid=True),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output("vehicle-dropdown", "value"),
    Input("vehicle-dropdown", "value"),
)
def handle_select_clear_all(selected_vehicles):
    if "SELECT_ALL" in selected_vehicles:
        return [str(vehicle) for vehicle in vehicles]
    elif "CLEAR_ALL" in selected_vehicles:
        return []
    return selected_vehicles

@app.callback(
    Output("vehicle-map", "figure"),
    [Input("vehicle-dropdown", "value"),
     Input("interval-component", "n_intervals")],
)
def update_map(selected_vehicles, n_intervals):

    if not selected_vehicles or "CLEAR_ALL" in selected_vehicles:
        return go.Figure()
    
    with conn.connect() as connection:
        df = pd.read_sql_query(sql=query, con=connection)
        df['measurement_time'] = pd.to_datetime(df['measurement_time'])  # Ensure measurement_time is datetime
        vehicles = list(df['vehicle_id'].unique())
        selected_vehicles = [v for v in vehicles if v not in ["SELECT_ALL", "CLEAR_ALL"]]


    
    dff = df[df['vehicle_id'].isin(selected_vehicles)]
    
    
    dff['rank'] = dff.groupby('vehicle_id')['measurement_time'].rank("dense", ascending=True)
    max_rank = dff['rank'].max()
    selected_rank = max_rank 
    dff = dff[dff['rank'] == selected_rank]

    fig = px.scatter_geo(dff, lat='latitude', lon='longitude',
                         hover_name='vehicle_id',
                         hover_data={'vehicle_id':True, 'measurement_sequence':True,'fuel_capacity':True, 'fuel_remaining_percent': True, 'measurement_time':True, 'distance_traveled':True},
                         projection="natural earth",
                         color='color',
                         color_discrete_map={'green': 'green', 'yellow': 'blue', 'orange': 'orange', 'red': 'red'})

    fig.update_geos(
    visible=False, resolution=50,
    showcountries=True, countrycolor="black"
)
    fig.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)


#%%


