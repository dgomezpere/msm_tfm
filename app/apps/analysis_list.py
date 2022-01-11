#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
from pymongo import MongoClient

# Analysis list data table

def load_analysis_list_df(db_name: str, collection_name: str):
    """
    """

    # Empty dataframe
    df = pd.DataFrame({
        'analysis_id': [],
        'analysis_name': [],
        'creation_date': [],
        'last_accession_date': [],
        'last_update_date': [],
        'curator_name': [],
        'analysis_progress': [],
        })

    # Colname mapping
    column_display_names_mapping = {
        'analysis_id': 'Analysis ID',
        'analysis_name': 'Analysis Name',
        'creation_date': 'Creation Date',
        'last_accession_date': 'Last Accession',
        'last_update_date': 'Last Update',
        'curator_name': 'Curator',
        'analysis_progress': 'Progress',
    }

    c = MongoClient()
    db = c[db_name]
    collection = db[collection_name]
    documents = list(collection.find())
    if len(documents) == 0: # If no DB available or empty DB, return empty dataframe
        return df
    else:
        # Update dataframe data with DB documents
        df = pd.DataFrame(documents)[df.columns]
        # Convert datetimes to human-readable format
        datetime_display_format = "%Y/%m/%d (%H:%M:%S)"
        df['creation_date'] = pd.DatetimeIndex(df['creation_date']).strftime(datetime_display_format)
        df['last_accession_date'] = pd.DatetimeIndex(df['last_accession_date']).strftime(datetime_display_format)
        df['last_update_date'] = pd.DatetimeIndex(df['last_update_date']).strftime(datetime_display_format)
        # Rename colnames with display names
        df = df.rename(column_display_names_mapping, axis=1)
        return df

analysis_list_df = load_analysis_list_df(db_name='somaticseeker', collection_name='analysis_list')

analysis_list_datatable = dash_table.DataTable(
    id='analysis_list_datatable',
    columns=[{'name': column, 'id': column, 'deletable': False, 'renamable': False} for column in analysis_list_df.columns],
    data=analysis_list_df.to_dict('records'),
    filter_action="native",
    sort_action="native",
    sort_mode='single',
    row_selectable='single',
    selected_rows=[],
    page_action='native',
    page_current= 0,
    page_size= 10,
    fill_width=True,
    export_format=None,
    export_headers='display',
    export_columns='visible',
    style_table={
        'maxHeight': '50ex',
        'overflowY': 'scroll',
        'overflowX': 'scroll',
        'width': 'auto',
        'marginLeft': '50px',
        'marginRight': '50px',
        'marginTop': '50px',
        'marginBottom': '50px',
    },
    style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white',
        'fontWeight': 'bold',
    },
)

# Buttons

button_style = {
    'marginLeft': '50px',
    'marginRight': '0px',
}

new_analysis_button = dbc.Button(
    "New Analysis",
    id='new_analysis_button',
    color="secondary",
    href="somatic_seeker/new_analysis",
    style=button_style,
)

view_analysis_button = dbc.Button(
    'View Analysis',
    id='view_analysis_button',
    color='secondary',
    href='somatic_seeker/view_analysis',
    disabled=True,
    style={'marginLeft': '10px'},
)

local_storage = dcc.Store(
    id='local_storage',
    storage_type='local'
)

# Callbacks

@app.callback(
    Output('analysis_list_datatable', component_property='data'),
    Input('analysis_list_datatable', component_property='data'),
)

def update_analysis_list_df(data):
    analysis_list_df = load_analysis_list_df(db_name='somaticseeker', collection_name='analysis_list')
    if len(data) != len(analysis_list_df):
        return analysis_list_df.to_dict(orient='records')
    else:
        return data

@app.callback(
    Output('selected_analysis', component_property='children'),
    [
        Input('analysis_list_datatable', component_property='data'),
        Input('analysis_list_datatable', component_property='selected_rows'),
    ]
)

def selected_analysis(data, selected_rows):
    if selected_rows:
        df = pd.DataFrame(data)
        selected_analysis_id = df.query(f"index in {selected_rows}").to_dict('records')[0]['Analysis ID']
        return selected_analysis_id

@app.callback(
    Output('view_analysis_button', component_property='disabled'),
    Input('analysis_list_datatable', component_property='selected_rows'),
)

def view_analysis_button_disabled(selected_rows):
    if selected_rows:
        disabled = False
    else:
        disabled = True
    return disabled

# Layout

h_style = {
    'text-align':'left',
    'marginLeft': '20px',
    'marginRight': '20px',
    'marginTop': '20px',
    'marginBottom': '20px',
    'fontWeight': 'bold',
}

layout = html.Div([
    html.H1('Somatic Seeker', style=h_style),
    html.Hr(),
    html.H2('Analysis List', style=h_style),
    analysis_list_datatable,
    new_analysis_button,
    view_analysis_button,
    html.Div(id='selected_analysis'),
])

