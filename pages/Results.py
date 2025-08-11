import dash
from dash import html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.graph_objs as go


def table_style_data_conditional(df_chosen):
    styles = [
        {"if": {"column_id": "Overall"}, "backgroundColor": "#f9f9f9"},
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': "#f9f9f9",
        },
        {
            'if': {'column_id': 'Name'},
            'textAlign': 'left'
        }
    ]
    return styles


dash.register_page(__name__)

data = pd.read_csv('./data/data.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.nan)

year_dropdown_labels = list(df['Year'].unique())
name_dropdown_labels = list(df['Name'].unique())

DATA_TABLE_STYLE = {
    "style_data_conditional": table_style_data_conditional(dcc.Store(id='df_chosen', data=[])),
    "style_header": {
        "color": "black",
        "backgroundColor": "#E6E6E6",
        "fontWeight": "bold",
    }
}


competition_card = \
dbc.Card([
    dbc.CardHeader(html.B("Select Data for Overall Results"),
                   style = {
                       "backgroundColor": "#f4e0ff"
                   }),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**1) Choose Year**'''),
                dcc.Dropdown(year_dropdown_labels,
                             id= 'year_dropdown',
                             searchable=False,
                             optionHeight=50,
                             placeholder= 'Select Year'
                             )

            ]),
        ])]),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**2) Choose Competition**'''),
                dcc.Dropdown(['Please Choose 1)'],
                             id= 'comp_dropdown',
                             searchable=True,
                             optionHeight=50,
                             style = {'white-space': 'nowrap', 'position': 'initial'},
                            placeholder= 'Select Competition'
                ),
            ]),
        ])]),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''**3) Choose Age Group**'''),
                dcc.Dropdown(['Please Choose 1) & 2)'],
                             id= 'age_dropdown',
                             searchable=True,
                             optionHeight=50,
                            placeholder= 'Select Age Group'
                ),
            ])
        ]),
        dbc.Row([
            dbc.CardBody([
                dbc.Button('Submit', id = 'comp_submit_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2"}
                ),
                dbc.Button('Reset', id = 'reset_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2", "color":"red"}
                ),
            ], style={'textAlign': 'center'})
        ])
    ])

])

results_card =  \
html.Div([
       dcc.Markdown('''''', id = 'data_markdown'),
                    html.Center([
                        dcc.Markdown('', id = 'table_title'),
                        dash_table.DataTable(id = 'table',
                            style_as_list_view=True,
                            sort_action = 'native',
                            style_data_conditional = DATA_TABLE_STYLE.get("style_data_conditional"),
                            style_header=DATA_TABLE_STYLE.get("style_header"),
                            style_cell = {'textAlign': 'center',
                                          'font-family':'sans-serif'},
                            style_table={'overflowX': 'auto',
                                'minWidth': '90vw', 'width': '90vw', 'maxWidth': '90vw'
                                        },
                            fixed_columns={'headers': True, 'data': 1},
                    )]),
        html.Br(),
        html.Center(dcc.Markdown('', id = 'graph_title')),
                dcc.Graph(
                    id = 'graph',
                    config= {'displayModeBar':False,
                            'modeBarButtonsToRemove': ['pan2d','lasso2d']
                            },
                    figure={
                        'data': [],
                        'layout': go.Layout(                                
                            xaxis =  {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False},
                            yaxis = {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False}                                                               
                            )
                        },
                    )
])
# dbc.Card([
#                 dbc.CardHeader(html.B("Results"),style = {
#                        "backgroundColor": "#f4e0ff"
#                    }),
#                 dbc.CardBody([
                    # dcc.Markdown('''Please select year, competition, and age group first.''', id = 'data_markdown'),
                    # html.Center([
                    #     dcc.Markdown('', id = 'table_title'),
                    #     dash_table.DataTable(id = 'table',
                    #         style_as_list_view=True,
                    #         sort_action = 'native',
                    #         style_data_conditional = DATA_TABLE_STYLE.get("style_data_conditional"),
                    #         style_header=DATA_TABLE_STYLE.get("style_header"),
                    #         style_cell = {'textAlign': 'center',
                    #                       'font-family':'sans-serif'},
                    #         style_table={'overflowX': 'auto',
                    #             'minWidth': '90vw', 'width': '90vw', 'maxWidth': '90vw'
                    #                     },
                    #         fixed_columns={'headers': True, 'data': 1},
                    # )]),
                # ]),
                # dbc.CardBody([
                    # html.Center(dcc.Markdown('', id = 'graph_title')),
                    # dcc.Graph(id = 'graph',
                    #     figure={
                    #         'data': [],
                    #         'layout': go.Layout(                                
                    #             xaxis =  {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False},
                    #             yaxis = {'showgrid': False, 'zeroline': False, 'ticks':'', 'showticklabels':False}                                                               
                    #             )
                    #         })
                    # dbc.Row(table_card),
                    # dbc.Row(plot_card)
                # ])
            # ], style= {"padding": "0px", "margin-bottom": "0.5em"}
# )

layout = html.Div([
    dbc.Container([
        html.Br(),
        competition_card,
        html.Br(),
        results_card
    ], fluid=True,
        style = {'minWidth': '96vw',
                    'width': '96vw',
                    'maxWidth': '96vw',
                    'align-items': 'center',
                    "height": "80vh"})
])



