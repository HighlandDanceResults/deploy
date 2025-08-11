import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

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

DATA_TABLE_STYLE = {
    "style_data_conditional": table_style_data_conditional(dcc.Store(id='df_chosen', data=[])),
    "style_header": {
        "color": "black",
        "backgroundColor": "#E6E6E6",
        "fontWeight": "bold",
    }
}

dash.register_page(__name__)

data = pd.read_csv('./data/data.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.nan)

year_dropdown_labels = list(df['Year'].unique())
name_dropdown_labels = sorted(list(df['Name'].unique()))


search_card = \
dbc.Card([
    dbc.CardHeader(html.B("Dancer Search"),
                   style = {
                       "backgroundColor": "#f4e0ff"
                   }),
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Markdown('''Search Dancer Name'''),
                dcc.Dropdown(name_dropdown_labels,
                             id= 'search_name_dropdown',
                             searchable=True,
                             optionHeight=50,
                             placeholder= 'Search or Select Name'
                             )

            ]),
        ]),
        dbc.Row([
            dbc.CardBody([
                dbc.Button('Submit', id = 'search_submit_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2"}
                ),
                dbc.Button('Reset', id = 'search_reset_btn', outline=True, color = 'dark', className="me-1",
                            style = {"backgroundColor": "#e1eaf2", "color":"red"}
                ),
            ], style={'textAlign': 'center'})
        ])
        ]),
])

results_card = html.Div([
    dcc.Markdown('''''', id = 'search_markdown'),
    html.Center([
        dcc.Markdown('', id = 'table_title'),
        dash_table.DataTable(id = 'search_table',
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
])

# dbc.Card([
    # dbc.CardHeader(html.B("Results"),style = {
    #         "backgroundColor": "#f4e0ff"
    #     }),
    # dbc.CardBody([

    # ])
# ])

layout = html.Div([
    dbc.Container([
        html.Br(),
        search_card,
        html.Br(),
        results_card
    ], fluid=True,
        style = {'minWidth': '96vw',
                    'width': '96vw',
                    'maxWidth': '96vw',
                    'align-items': 'center',
                    "height": "80vh"})
])