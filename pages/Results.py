import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


dash.register_page(__name__)

data = pd.read_csv('./data/data.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.nan)

year_dropdown_labels = list(df['Year'].unique())
name_dropdown_labels = list(df['Name'].unique())



competition_card = \
dbc.Card([
    dbc.CardHeader(html.B("Select Data for Overall Results"),
                   style = {
                       "background-color": "#f4e0ff"
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
                dcc.Dropdown(['test comp'],
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
                dcc.Dropdown(['test age'],
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



layout = html.Div([
    dbc.Container([
        html.Br(),
        competition_card
    ], fluid=True,
        style = {'minWidth': '96vw',
                    'width': '96vw',
                    'maxWidth': '96vw',
                    'align-items': 'center',
                    "height": "80vh"})
])


