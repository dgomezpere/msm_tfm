import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server
from apps import app0, app1, app2, app3, app4, app5

layout = html.Div(dcc.Link('Navigate to Webpage',
href = 'http://127.0.0.1:5000/new_project', target='_blank'))
