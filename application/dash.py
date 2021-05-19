import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio
import numpy as np
import dash_table
import sidetable as stb
import datetime
from datetime import datetime, timedelta
from datetime import date
import geopandas as gpd
import flask
import os

base = pd.read_csv("https://sniiv.conavi.gob.mx/doc/datos_abiertos/financiamientos/202011.csv", encoding='latin-1')
# Usa un shapefile !!
geo_mpios=gpd.read_file('mpios_clear.shp')
geo_mpios.columns

listameses = [ 'Organismo', 'Modalidad',
       'Destino del Credito', 'Tipo de Credito', 'Genero', 'Rango de Edad',
       'Rango de Ingresos UMA', 'Valor de la Vivienda', 'Acciones', 'Monto']

#lista de las semanas 
fnameDict = listameses
names = list(fnameDict)


bfinal = geo_mpios.merge(base, left_on=(['NOM_MUN','NOM_ENT']), right_on=(['Municipio','Entidad Federativa']), how= "left" )
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
    
        dbc.Row(
            [
           
           dbc.Col(dcc.Dropdown(
           id="slct_year",
           options=[{'label':name, 'value':name}
                 for name in names],
           value = list(fnameDict)[0]),
                width={'size' : 6,'offset' : 1 },
                  style={'text-size': 28}),


        #style={'width': '70%', 'display': 'inline-block'},
        #),
       html.Div(id='output_container', children=[])]),
       html.Br(),
        
    dbc.Row(
        [
        dbc.Col(dcc.Graph(id='my_bee_map', figure={},
                      style={'width': '50rem', 
                             'display': 'inline-block',
                            'align': 'center'}))]),
])
        # Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
    )
def update_graph(option_slctd):
    
    print(option_slctd)
    print(type(option_slctd))
        
    container = "Variable seleccionada: {}".format(option_slctd)
        
        
    semnalgraph =  px.choropleth_mapbox(bfinal[(option_slctd)],
                                   geojson=bfinal.geometry,
                                   locations=bfinal.index,
                                   color= (option_slctd),
                                   range_color=[100, 1500],     
                                   center={"lat": 23.88234, "lon": -102.28259},
                                   mapbox_style="carto-positron",
                                   zoom= 4.5,
                                   opacity=.6,
                                   color_continuous_scale=px.colors.sequential.Oranges,
      
                                       )     

    
    semnalgraph.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        autosize=False,
        width=1200,
        height=700,
        showlegend = False
            )
    
    return container, semnalgraph


#])

app.layout = html.Div([body])

#from application.dash import app
#from settings import config

if __name__ == "__main__":
    app.run_server()
