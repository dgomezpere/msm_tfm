import dash
import dash_bootstrap_components as dbc

#Create the server with BOOTSTRAP theme
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
