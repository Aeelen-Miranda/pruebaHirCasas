import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
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

yesterday = datetime.now() - timedelta(1)
yea = datetime.strftime(yesterday, '%Y%m%d')

today = date.today()
d2 = today.strftime("Fecha de actualización : %d-%m-%Y")


base = pd.read_csv("https://sniiv.conavi.gob.mx/doc/datos_abiertos/financiamientos/202011.csv", encoding='latin-1')

#Seleccionar Entidad
cdmx = base[base["Entidad Federativa"]== "Ciudad de México"]

#Selecciona columnas
patabla= cdmx[['Monto','Municipio']]#.astype(int)
#Convert str to int
#patabla[['Monto']] = patabla[['Monto']].astype(int)
patabla["Monto"] = [float(str(i).replace(",", "")) for i in patabla["Monto"]]
#patabla["Monto"] = [float(str(i).replace(".", "")) for i in patabla["Monto"]]


#   identificadores
tot_cdmx = patabla.Monto.sum()
#print ("Monto total de Ciudad de México :    ", tot_cdmx)


#Por alcaldía abs
alca_1 = patabla[patabla.Municipio == "Xochimilco"].Monto.sum()
alca_2 = patabla[patabla.Municipio == "Venustiano Carranza"].Monto.sum()
alca_3 = patabla[patabla.Municipio == "Tlalpan"].Monto.sum()
alca_4 = patabla[patabla.Municipio == "Tláhuac"].Monto.sum()
alca_5 = patabla[patabla.Municipio == "Milpa Alta"].Monto.sum()
alca_6 = patabla[patabla.Municipio == "Miguel Hidalgo"].Monto.sum()
alca_7 = patabla[patabla.Municipio == "La Magdalena Contreras"].Monto.sum()
alca_8 = patabla[patabla.Municipio == "Iztapalapa"].Monto.sum()
alca_9 = patabla[patabla.Municipio == "Iztacalco"].Monto.sum()
alca_10 = patabla[patabla.Municipio == "Gustavo A. Madero"].Monto.sum()
alca_11 = patabla[patabla.Municipio == "Cuauhtémoc"].Monto.sum()
alca_12 = patabla[patabla.Municipio == "Cuajimalpa de Morelos"].Monto.sum()
alca_13 = patabla[patabla.Municipio == "Coyoacán"].Monto.sum()
alca_14 = patabla[patabla.Municipio == "Benito Juárez"].Monto.sum()
alca_15 = patabla[patabla.Municipio == "Azcapotzalco"].Monto.sum()
alca_16 = patabla[patabla.Municipio == "Álvaro Obregón"].Monto.sum()
alca_17 = patabla[patabla.Municipio == "No distribuido"].Monto.sum()

#percent
alca_p1= (alca_1/tot_cdmx)*100
alca_p2= (alca_2/tot_cdmx)*100
alca_p3= (alca_3/tot_cdmx)*100
alca_p4= (alca_4/tot_cdmx)*100
alca_p5= (alca_5/tot_cdmx)*100
alca_p6= (alca_6/tot_cdmx)*100
alca_p7= (alca_7/tot_cdmx)*100
alca_p8= (alca_8/tot_cdmx)*100
alca_p9= (alca_9/tot_cdmx)*100
alca_p10= (alca_10/tot_cdmx)*100
alca_p11= (alca_11/tot_cdmx)*100
alca_p12= (alca_12/tot_cdmx)*100
alca_p13= (alca_13/tot_cdmx)*100
alca_p14= (alca_14/tot_cdmx)*100
alca_p15= (alca_15/tot_cdmx)*100
alca_p16= (alca_16/tot_cdmx)*100
alca_p17= (alca_17/tot_cdmx)*100
#Agrupa alcaldias
patabla.groupby(['Municipio'])['Monto'].sum().to_csv('0000procesotabla.csv')
#Abrir
tabla = pd.read_csv("0000procesotabla.csv")
#Dtypes again
tabla['Monto']=tabla['Monto'].astype(int)

#ordenar de mayor a menor 
tmun = tabla.sort_values(by='Monto', ascending=False)


#mpios
alcaldia1=tmun.iloc[0]['Municipio']
alcaldia2=tmun.iloc[1]['Municipio']
alcaldia3=tmun.iloc[2]['Municipio']
alcaldia4=tmun.iloc[3]['Municipio']
alcaldia5=tmun.iloc[4]['Municipio']

#montos
alcaldia1m=tmun.iloc[0]['Monto']
alcaldia2m=tmun.iloc[1]['Monto']
alcaldia3m=tmun.iloc[2]['Monto']
alcaldia4m=tmun.iloc[3]['Monto']
alcaldia5m=tmun.iloc[4]['Monto']


bllt =("Las 5 alcaldias con más monto son: "+
   #   f"{int(pobzmguadalajara):,}"
          alcaldia1+" ("+f"{int(alcaldia1m):,}" +"), "+
          alcaldia2+" ("+f"{int(alcaldia2m):,}" +"), "+
          alcaldia3+" ("+f"{int(alcaldia3m):,}" +"), "+
          alcaldia4+" ("+f"{int(alcaldia4m):,}" +"), "+

          "y "+
          alcaldia5+" ("+f"{int(alcaldia5m):,}" +").")
#print(bllt)

#Grafica mpal 
graf_meses = go.Figure()
graf_meses.add_trace(go.Bar(x=tabla["Municipio"],y=tabla['Monto'],
                marker_color='indianred'  
                ))
graf_meses.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_tickangle=-45,
    template = 'simple_white',
    title='',
    xaxis_tickfont_size= 12,
    yaxis=dict(
        title='Distribución de monto por municipio',
        titlefont_size=14,
        tickfont_size=12,
        titlefont_family= "Monserrat"),
    )
########### Define your variables


server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes. LUX], server=server)

body = html.Div([
    html.Br(),
    html.Br(),
        dbc.Row(
           [dbc.Col(html.H1("PRUEBA TÉCNICA ANALISTA DE MODELOS."),
                        width={'offset' : 2})]),
        dbc.Row(
           [
            dbc.Col(html.H3("breve analisis de la Ciudad de México. por Aeelen Miranda"),
                   width={'offset' : 2}),]),
  
    dbc.Row(
           [dbc.Col(html.H6(d2),           #Fecha de actualización
               width={'size' : "auto",
                      'offset' : 4}),]),
    
    

    html.Br(),
    html.Br(),
     html.Br(),
    html.Br(),
    dbc.Row(
        [
            
            dbc.Col(dbc.Button(([html.P("El monto total de Noviembre 2020 fue de: "), 
                 html.P(f"{int(tot_cdmx):,}",  
                        style={
                               "color": "dark", 
                               #"font-weight": 'bold',
                               "font-size": "40px",
                               "font-family": "Montserrat",        
                               #"font-weight": 'bold'
                        }),                      
       ]),style={ "background-color": "light",
                  "box-shadow": "10px 20px 30px gray",
                  'margin-left': '100px',
                 } ,disabled=True)),
        dbc.Col(html.H4("Las 5 alcaldías que reflejaron más monto en noviembre de 2020 fueron: Álvaro Obregón (1,415,693,516), "
                        "Benito Juárez (664,855,746), Miguel Hidalgo (503,817,990), Cuauhtémoc (347,362,316), y Coyoacán "
                        "(293,227,848)."))
        ]),
    
     html.Br(),
     html.Br(),
    html.Br(),
    
         dbc.Row(
        [
            
            dbc.Col(dbc.CardImg(src="https://github.com/Aeelen-Miranda/pruebaHirCasas/blob/main/cdmx.jpeg?raw=true")),
            dbc.Col(dcc.Graph(figure=graf_meses, ),
                   width={"size": 6})
        ]),
    #Tabla 
       dbc.Row(
               [dbc.Col(dash_table.DataTable(
               id='table',
           columns=[{"name": i, "id": i} for i in tmun.columns],
           data=tmun.to_dict('records'),
                   fixed_rows={'headers': True,"striped": True,},
                   style_table={'height': '300px', 'overflowY': 'auto',"striped": True,},
                   style_cell={'fontSize':12, 'font-family':'Nunito Sans',"striped": True,}, 
                   style_header = {'border': 'none','fontWeight': 'condensed'},
                   style_data = {'border': 'none', "striped": True, },
                   style_data_conditional=[{'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(248, 248, 248)'}],
               ), style={
           'margin-top': '9px',
           'margin-left': '100px',
           'margin-right': '0px',
           'width': '750px',
                  
               })]),
    
    html.Br(),
    html.Br(),
    html.Br(),
        
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H5("Para el ejercicio #2: Se propone el modelo de regresión lineal múltiple de plotly, "
                        " Scikit-learn es una biblioteca popular de aprendizaje automático (ML)"
                        " funciona para predecir las tendencias que en función del valor total."
                        " Además de la regresión lineal, es posible ajustar los mismos datos utilizando"
                        " k-Vecinos más cercanos"),
                style={"color": "black", 
                            "font-size": "14px",
                            "font-family": "Arial",   
                            "background-color": "lightgray"})
    ], style={"background-color": "lightgray",
                          "box-shadow": "10px 20px 30px gray",
                           'width': '1100px',
                           'margin-left': '100px',
                           'margin-right': '0px'}),
        
    html.Br(),
    html.Br(),
    html.Br(),
        
    html.Br(),
    html.Br(),
    html.Br(),
])
app.layout = html.Div([body])

#from application.dash import app
#from settings import config

if __name__ == "__main__":
    app.run_server()
