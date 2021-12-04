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
    html.H1('Somatic Seeker', style={'color': 'darkblue', 'margin-left': '30px'}),
    html.Hr(),
    html.H2('Analysis', style={'margin-left': '30px'}),
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
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
        fill_width=True,
        style_table={
        'maxHeight': '50ex',
        'overflowY': 'scroll',
        'overflowX': 'scroll',
        'width': '1850px',
        'marginLeft': '30px'
        },
    ),
    html.Div(id='datatable-row-ids-container'),

    dcc.Link(dbc.Button('View Analysis', style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '30px','margin-left': '100px'
    }), href='/apps/app3'),

    dbc.Button('Delete Analysis', id="delete_analysis", style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '30px','margin-left': '100px'
    }, n_clicks=0),

    dcc.Link(dbc.Button('Run New Analysis', style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '160px',
    'margin-top': '30px','margin-left': '100px'
    }), href='/apps/app3'),

    dcc.Download(id="download-list"),
    html.Div(id='output'),
    html.Div(id='datatable-row-ids-selection')

])

@app.callback(
    Output("download-list", "data"),
    Input("btn_download_list", "n_clicks"),
    prevent_initial_call=True)
def download_table(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf_csv.csv")

@app.callback(Output('output', 'children'),
              [Input('datatable-row-ids', 'data_previous')],
              [State('datatable-row-ids', 'data')])
def show_removed_rows(previous, current):
    if previous is None:
        dash.exceptions.PreventUpdate()
    else:
        return [f'Just removed {row}' for row in previous if row not in current]

# @app.callback(
#     Output('datatable-row-ids-selection', 'children'),
#     [State('datatable-row-ids', 'derived_virtual_row_ids'),
#     State('datatable-row-ids', 'selected_row_ids'),
#     Input('delete_analysis', 'n_clicks')])
# def delete_id(selected_row_ids, row, n_clicks):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     if 'delete_analysis' in changed_id:
#         return row

@app.callback(
    Output('datatable-row-ids', 'data'),
    [State('datatable-row-ids', 'derived_virtual_row_ids'),
    State('datatable-row-ids', 'selected_row_ids'),
    Input('delete_analysis', 'n_clicks')])
def delete_id(selected_row_ids, row, n_clicks):
    dff=df
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()
    else:
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        dff=dff.drop(row, axis=0)
        if 'delete_analysis' in changed_id:
            return dff.to_dict('records')
