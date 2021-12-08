import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from app import server
from apps import app0, app1, app2, app3, app4

# Define button style
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

#Start layout
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
#Create Ran analysis button. When it is clicked the analysis is started and
#a new window is opened with panoptes running
    dcc.Link(dbc.Button('Run Analysis', id='run_analysis',
    style=blue_button_style, n_clicks= 0),
    href='http://127.0.0.1:5000/new_project',
    target='_blank'),
    html.Div(id='page_content')
])

#Start a callbak to change the color of Run analysis button when it is clicked
@app.callback(
    Output("run_analysis", "style"),
    [Input("run_analysis", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return grey_button_style

    else:
        return blue_button_style

#Start a callback to generate a new button to proceed with the analysis
#once the pipeline ends
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
