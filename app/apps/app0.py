import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

import flask
from datetime import date
import pandas as pd


import datetime
import base64
import io

layout = html.Div([
    html.H1('Somatic Seeker', style={'color': 'darkblue'}),
    html.Hr(),
    dcc.Link('Start new project', href='/apps/app1'),
    html.Br(),
    dcc.Link('Load previous project', href='/apps/app2'),
])
