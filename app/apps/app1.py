import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from app import server
from apps import app0, app1, app2, app3, app4, app5

import flask
from datetime import date
import pandas as pd


import datetime
import base64
import io

grey_button_style={'background-color': 'grey', 'borderColor': 'grey',
'height': '50px','width': '140px',
'margin-top': '20px','margin-left': '100px'
}

green_button_style={'background-color': 'green', 'borderColor': 'green',
'height': '50px','width': '140px',
'margin-top': '20px','margin-left': '100px'
}

blue_button_style={'background-color': 'darkblue', 'borderColor': 'darkblue',
'height': '50px','width': '140px',
'margin-top': '20px','margin-left': '100px'
}




layout = html.Div([
    html.H1('Somatic Seeker', style={'color': 'darkblue',
    'margin-left': '30px', 'margin-top': '15px'}),
    html.Hr(),
    html.H2('New analysis',
    style={'margin-left': '30px'}),
    html.Hr(),
    html.H4('Analysis name',
    style={'margin-left': '30px'}),
    dcc.Input(id='input-2-state', value='My Project',
    style={'margin-bottom':'30px',
    'background-color': 'lightgrey', 'margin-left': '30px',
    'margin-top': '15px'}),
    html.H4('Curator name',
    style={'margin-left': '30px'}),
    dcc.Input(id='input-3-state', value='Curator',
    style={'margin-bottom':'30px',
    'background-color': 'lightgrey', 'margin-left': '30px',
    'margin-top': '15px'}),
    html.H4('VCF file',
    style={'margin-left': '30px'}),
    dcc.Upload(
        id='input-1-state',
        children=html.Div([dbc.Button('Upload VCF',
        id="upload_vcf",
        className="mt-3",
        style={'margin-bottom':'30px', 'margin-left': '30px'})
    ]),
    ),
    html.H4('Reference Genome',
    style={'margin-left': '30px'}),
    dcc.Upload(
        id='input-4-state',
        children=html.Div([dbc.Button('Upload Reference FASTA file',
        id="upload_refgenome",
        className="mt-3",
        style={'margin-bottom':'20px', 'margin-left': '30px'})
    ]),
    ),
    #html.Div(id='output-state'),
    dcc.Link(dbc.Button('Run Analysis', id='run_analysis',
    style=blue_button_style, n_clicks= 0),
    href='http://127.0.0.1:5000/new_project',
    target='_blank'),
    html.Div(id='page_content')
])

@app.callback(Output('output-state', 'children'),
              Input('input-1-state', 'contents'),
              Input('input-1-state', 'filename'),
              Input('input-1-state', 'last_modified'))

def return_output(contents, filename, last_modified):
    try:
        if 'txt' in filename:
            return html.Div([
            html.H5(base64.b64decode(contents.split(',')[1]).decode('utf-8')), #Decode and recode to utf-8
            html.H5(filename),
            html.H5(datetime.datetime.fromtimestamp(last_modified).date()) #From just seconds to date
            ])
        else:
            return html.Div([
            html.H5("ERROR Upload a .txt file")
            ])
    except:
        return html.Div([
        html.H5("Upload a .txt file")
        ])

@app.callback(
    Output("run_analysis", "style"),
    [Input("run_analysis", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return grey_button_style

    else:
        return blue_button_style

@app.callback(
    Output("page_content", "children"),
    [Input("run_analysis", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return html.Div([
            dcc.Link(dbc.Button('View Results', id='view_results',
            style=green_button_style),
            href='/apps/app4')])
