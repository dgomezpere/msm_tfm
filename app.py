# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#Dash Modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dtab
from dash.dependencies import Input, Output, State

import flask
from datetime import date

#uploading dash_table
import datetime
import base64
import io


app = dash.Dash(__name__)

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

layout_index = html.Div([
    html.H1('VCF Pepito Annotator App'),
    html.Hr(),
    dcc.Link('Start new project', href='/new_project'),
    html.Br(),
    dcc.Link('Load previous project', href='/previous_project'),
])

#https://dash.plotly.com/dash-core-components/upload
layout_page_1 = html.Div([
    html.H1('VCF Pepito Annotator App'),
    html.Hr(),
    html.H2('Load new project'),
    dcc.Upload(
        id='input-1-state',
        children=html.Div(['Drag and Drop or ',
        html.A('Select a File')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    }),

    html.Div(id='output-state'),

    html.H4('Project name'),
    dcc.Input(id='input-2-state', value='Project'),
    html.H4('Date'),
    dcc.DatePickerSingle(
        date=date.today(),
        display_format='D-M-Y'
        ),
    html.H4('Curator name'),
    dcc.Input(id='input-3-state', value='Curator'),
    html.Hr(),
    dcc.Link('Next', href='/loading'),
    html.Br(),
    dcc.Link('Return', href='/'),
])

#Show previous data bases. for loop i->database_name
layout_page_2 = html.Div([
    html.H1('VCF Pepito Annotator App'),
    html.Hr(),
    html.H2('Previous Projects'),
    dcc.Dropdown(
        options=[
            {'label': 'cMyc Study', 'value': 'cMyc'},
            {'label': 'MAPK draft analysis', 'value': 'MAPK'},
            {'label': 'new Pepito gene', 'value': 'Pepito'}
        ],
        value= 'cMyc',
        multi=True
    ),
    html.Div(id='page-2-display-value'),

    html.Hr(),
    dcc.Link('Next', href='/loading'),
    html.Br(),
    dcc.Link('Return', href='/'),
])

layout_page_3 = html.Div([
    html.H1('VCF Pepito Annotator App'),
    html.Hr(),
    html.H2('Loading'),
    html.Hr(),
    dcc.Link('Next', href='/main_page')
])

layout_page_4 = html.Div([
    html.H1('VCF Pepito Annotator App'),
    html.Hr(),
    html.H2('Project name'),
    html.Hr(),
    dcc.Link('Next', href='/'),
    html.Br(),
    dcc.Link('Return', href='/')
])

# index layout
app.layout = url_bar_and_content_div

# # "complete" layout
# app.validation_layout = html.Div([
#     url_bar_and_content_div,
#     layout_index,
#     layout_page_1,
#     layout_page_2,
# ])


# Index callbacks
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/new_project":
        return layout_page_1
    elif pathname == "/previous_project":
        return layout_page_2
    elif pathname == "/loading":
        return layout_page_3
    elif pathname == "/main_page":
        return layout_page_4
    else:
        return layout_index


# Page 1 callbacks
# def read_test_file(filename):
#     with open(filename) as f:
#         data = f.read()
#     return data

@app.callback(Output('output-state', 'children'),
              Input('input-1-state', 'contents'),
              Input('input-1-state', 'filename'),
              Input('input-1-state', 'last_modified'))
def return_output(contents, filename, last_modified):
    return html.Div([
    html.H5(base64.b64decode(contents.split(',')[1]).decode('utf-8')), #Decode and recode to utf-8
    html.H5(filename),
    html.H5(datetime.datetime.fromtimestamp(last_modified).date()) #From just seconds to date
    ])



# Page 2 callbacks
# @app.callback(Output('page-2-display-value', 'children'),
#               Input('page-2-dropdown', 'value'))
# def display_value(value):
#     print('display_value')
#     return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
