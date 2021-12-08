import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    html.H1('Somatic Seeker', style={'color': 'darkblue'}),
    html.Hr(),
    dcc.Link('Start new project', href='/apps/app1'),
    html.Br(),
    dcc.Link('Load previous project', href='/apps/app2'),
])
