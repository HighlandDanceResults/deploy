import dash
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

# layout = html.Div([
#     html.H1('This is our Home page'),
#     html.Div('This is our Home page content.'),
# ])

layout = \
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Center(
                    html.Img(src = 'assets/dance_shoes_black.png',
                        alt = 'image',
                        style={
                            "height":"90vh",
                            "width":"auto"
                               }
                        ),
                ),
                # html.P([print(page['relative_path'])for page in dash.page_registry.values()])
                ]
            ,width = 4
            ),
            dbc.Col(
                dbc.Card(
                    [
                    dbc.CardHeader('Wecome to the Unofficial Highland Dance Results Page!',
                                   style = {
                                       "backgroundColor": "#f4e0ff"
                                   }),
                    dbc.CardBody(
                            dcc.Markdown('''                              
                                Checkout [scotdance.app] (https://scotdance.app/#/competitions/), which also has a mobile app! This website originated because some comps do not use the app.

                        
                                Email with results or corrections at <highlanddanceresults@gmail.com>. This is a passion project maintained by a single person in my free time. Please by nice :) 
                                ''')
                            ),
                    ],
                        style={
                            #    "width":"70%"
                               }
                    ),
                    width = 8
            ),
            
        ],
        align="center",
        justify="center",
    style={
        "height":"90vh",
        })

    ], fluid = True)