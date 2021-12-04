import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

import flask
from datetime import date
import pandas as pd

from app import app
from app import server
from apps import app0, app1, app2, app3, app4, app5

# #https://dash.plotly.com/datatable/callbacks
#
# #JSON instead of csv

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

PAGE_SIZE = 5

layout = html.Div(
    className="row",
    children=[
        html.H1('Somatic Seeker', style={'color': 'darkblue'}),
        html.Hr(),
        html.Div(
                dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                page_current=0,
                page_size=500,
                page_action='custom',

                editable=True,
                column_selectable="single",
                row_deletable=True,
                row_selectable="multi",
                selected_columns=[],
                selected_rows=[],

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[],
                export_format='xlsx',
                export_headers='display',
                export_columns='visible',
                merge_duplicate_headers=True
            ),
            style={'height': 750, 'overflowY': 'scroll'},
            className='six columns'
        ),
        html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        ),
    html.Br(),
    # dcc.Checklist( id='datatable-use-page-count',
    # options=[{'label': 'Use page_count', 'value': 'True'}],
    # value=['True']),'Page count: ',
    # dcc.Input(id='datatable-page-count',
    # type='number',
    # min=1,
    # max=29,
    # value=20)
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

# @app.callback(
#     Output('table-paging-with-graph', 'page_count'),
#     Input('datatable-use-page-count', 'value'),
#     Input('datatable-page-count', 'value'))
# def update_table(use_page_count, page_count_value):
#     if len(use_page_count) == 0 or page_count_value is None:
#         return None
#     return page_count_value
