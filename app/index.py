#Import required dash components and modules
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#Import app scripts
from app import app
from app import server
from apps import app0, app1, app2, app3, app4

#Start layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#Callback to start the differnt views of the app
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    elif pathname == '/apps/app4':
        return app4.layout
    else:
        return app0.layout

if __name__ == '__main__':
    app.run_server(debug=True)
