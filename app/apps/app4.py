import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import pandas as pd

from app import app
from app import server
from apps import app0, app1, app2, app3, app4

# #https://dash.plotly.com/datatable/callbacks

# #JSON instead of csv
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

PAGE_SIZE = 5

#Layout is a loading table. It is possible to select how any entries are shown.
layout = html.Div(
    className="row",
    children=[
        html.H1('Somatic Seeker', style={'color': 'darkblue'}),
        html.Hr(),
        html.H2('Analysis name'),
        html.Div(
                dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',
                editable=True,
                column_selectable="single",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                fill_width=False,
                style_table={
                'maxHeight': '50ex',
                'overflowY': 'scroll',
                'overflowX': 'scroll',
                'width': '950px',
                'marginLeft': '30px'
                },
                filter_action='custom',
                filter_query='',
                sort_action='custom',
                sort_mode='multi',
                sort_by=[],
                export_format='xlsx',
                export_headers='display',
                export_columns='visible',
                merge_duplicate_headers=True,

            ),
            style={'height': 500, 'overflowY': 'scroll'},
            className='six columns'
        ),
        html.Div(
            id='table-paging-with-graph-container',
            className="four columns"
        ),
    html.H6('Number of Variants',
    style={'margin-left': '25px', 'color':'darkblue'
    }),
    dcc.Input(id='datatable-page-size',
    type='number', min=1, value=20,
    style={'margin-left': '40px', 'width': '80px'})
    ])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

#Callback to filter, edit the number of records shown and sort the datatable
@app.callback(
    Output('table-paging-with-graph', "data"),
    Input('table-paging-with-graph', "page_current"),
    Input('table-paging-with-graph', "page_size"),
    Input('table-paging-with-graph', "sort_by"),
    Input('table-paging-with-graph', "filter_query"))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')
