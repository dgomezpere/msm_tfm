# import dash_core_components as dcc
# import dash_html_components as html
# import dash_table
#
# import time
#
from app import app
from app import server
from apps import app0, app1, app2, app3, app4
#
# import dash_bootstrap_components as dbc
# from dash import Input, Output, html
#
# layout = html.Div(
#     [
#         dbc.Button("Load", id="loading-button", n_clicks=0),
#         dbc.Progress(html.Div(id="loading-output"))
#     ]
# )
#
#
# @app.callback(
#     Output("loading-output", "children"), [Input("loading-button", "n_clicks")]
# )
# def load_output(n):
#     if n:
#         time.sleep(3)
#         return f"Output loaded {n} times"
#     return "Output not reloaded yet"

import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

grey_button_style={'margin-top': '20px', 'margin-left': '30px',
'display': 'inline-block', 'background-color': 'grey',
'borderColor': 'grey'
}

green_button_style={'margin-top': '20px', 'margin-left': '30px',
'display': 'inline-block', 'background-color': 'green',
'borderColor': 'green'
}

layout = html.Div(
    [
        dbc.Progress([
            dbc.Progress(value=20, color="success", bar=True),
            dbc.Progress(value=30, color="warning", bar=True),
            dbc.Progress(value=20, color="danger", bar=True),
        ],
        style={'margin-top': '20px', 'margin-left': '30px',
        'margin-bottom': '50px'
        }),
        dbc.Button(
            "Variant decomposition",
            id="variant_decomposition",
            className="mt-3",
            style=grey_button_style, n_clicks=0),

        dbc.Button(
            "Variant normalization",
            id="variant_normalization",
            className="mt-3",
            style=grey_button_style, n_clicks=0),

        dbc.Button(
            "Variant annotation",
            id="variant_annotation",
            className="mt-3",
            style=grey_button_style, n_clicks=0),

        dbc.Button(
            "Creating database",
            id="creating_database",
            className="mt-3",
            style=grey_button_style, n_clicks=0),
    ]
)


@app.callback(
    Output("variant_decomposition", "style"),
    [Input("variant_decomposition", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return green_button_style

    else:
        return grey_button_style

@app.callback(
    Output("variant_normalization", "style"),
    [Input("variant_normalization", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return green_button_style

    else:
        return grey_button_style

@app.callback(
    Output("variant_annotation", "style"),
    [Input("variant_annotation", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return green_button_style

    else:
        return grey_button_style

@app.callback(
    Output("creating_database", "style"),
    [Input("creating_database", "n_clicks")
    ])
def change_button_color(n_clicks):
    if n_clicks > 0:
        return green_button_style

    else:
        return grey_button_style
