import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


import flask
from datetime import date
import pandas as pd

from app import app
from app import server
from apps import app0, app1, app2, app3, app4

import datetime
import base64
import io

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df['id'] = df['country']
df.set_index('id', inplace=True, drop=False)

layout = html.Div([
    html.H1('Somatic Seeker', style={'color': 'darkblue'}),
    html.Hr(),
    html.H2('Analysis'),
    dash_table.DataTable(
        id='datatable-row-ids',
        columns=[
            {'name': i,
            'id': i,
            'deletable': False,
            'renamable': False
            } for i in df.columns
            # omit the id column
            if i != 'id'
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='single',
        row_selectable='single',
        row_deletable=True,
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-row-ids-container'),

    dcc.Link(dbc.Button('Run Analysis', style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '30px','margin-left': '100px'
    }), href='/apps/app3'),

    dbc.Button('Download List', id='btn_download_list',
    style={'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '30px','margin-left': '100px'
    }, n_clicks=0),
    dcc.Download(id="download-list"),
])

@app.callback(
    Output("download-list", "data"),
    Input("btn_download_list", "n_clicks"),
    prevent_initial_call=True)

def download_table(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf_csv.csv")
