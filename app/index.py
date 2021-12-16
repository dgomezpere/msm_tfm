#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from dash import html, dcc
from dash.dependencies import Input, Output

from app import app
from apps import analysis_list, new_analysis, view_analysis

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    if pathname == '/somatic_seeker':
        return analysis_list.layout
    elif pathname == '/somatic_seeker/new_analysis':
        return new_analysis.layout
    elif pathname == '/somatic_seeker/view_analysis':
        return view_analysis.layout
    else:
        return '404' # Return html error 404 not found

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
