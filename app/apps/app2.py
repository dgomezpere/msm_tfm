import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import pandas as pd

from app import app
from app import server
from apps import app0, app1, app2, app3, app4

#Start an example dataframe
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df['id'] = df['country']
df.set_index('id', inplace=True, drop=False)

#Start layout to show a table with the differnt analysis done
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
        filter_action="native",
        sort_action="native",
        sort_mode='single',
        row_selectable='single',
        selected_rows=[],
        page_action='native',
        page_current= 0,
        page_size= 10,
        fill_width=True,
        export_format='xlsx',
        export_headers='display',
        export_columns='visible',
        style_table={
        'maxHeight': '50ex',
        'overflowY': 'scroll',
        'overflowX': 'scroll',
        'width': '1850px',
        'marginLeft': '30px'
        },
    ),
    html.Div(id='datatable-row-ids-container'),

#Create a button to visualize the result of a previous analysis
    dcc.Link(dbc.Button('View Analysis', style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '10px','margin-left': '100px'
    }), href='/apps/app3'),

#Create a button to confirm the deletion of a previous analysis
    dbc.Button('Delete Analysis', id="delete_analysis", style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '140px',
    'margin-top': '10px','margin-left': '100px'
    }, n_clicks=0),

#Create a button to repeat the analysis from a previous data analysis
    dcc.Link(dbc.Button('Run New Analysis', style={
    'display': 'inline-block', 'background-color': 'darkblue',
    'borderColor': 'darkblue',
    'height': '50px','width': '160px',
    'margin-top': '10px','margin-left': '100px'
    }), href='/apps/app3'),
])

#Create a callback delete a row after selecting it and clicking Delete analysis
@app.callback(
    Output('datatable-row-ids', 'data'),
    [State('datatable-row-ids', 'derived_virtual_row_ids'),
    State('datatable-row-ids', 'selected_row_ids'),
    Input('delete_analysis', 'n_clicks')])
def delete_id(selected_row_ids, row, n_clicks):
    global df
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()
    else:
        #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        df=df.drop(row, axis=0)
        #if 'delete_analysis' in changed_id:
        return df.to_dict('records')
        n_clicks = 0
