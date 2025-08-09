import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import pandas as pd
import numpy as np

data = pd.read_csv('./data/data.csv', keep_default_na=False)
df = pd.DataFrame(data)
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df = df.replace('', np.nan)

year_dropdown_labels = list(df['Year'].unique())
name_dropdown_labels = list(df['Name'].unique())

app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

page_names = ['Home',
              'Overall Results',
              'Dancer Search',
              'Judge\'s Points']
page_paths = ['Home',
              'Results',
              'Search',
              'JudgeResults'
              ]

navbar = dbc.NavbarSimple(
    children=[
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        page_names[i],
                        href = dash.page_registry[f'pages.{page_paths[i]}']['path'],
                        style={'color': "#ffffff"}
                    )
                ) for i in range(len(page_names))
            ]+
            [html.Img(src = 'assets/dance_shoes_white.png', alt = 'image', height = '40px')]
        )
    ],
    brand="Unofficial Highland Dance Results",
    # color="#a06cd5",
    color = "#22a6a7",
    dark=True,
)

app.layout = html.Div([
    dcc.Store(id='df_store', data=df.to_dict('records')),
    dcc.Store(id='df_chosen', data=[]),
    # dcc.Store(id='competition_cards_store', data=competition_card),
    navbar,
    dash.page_container
])
app.title = 'HD Results'

@app.callback(
    Output('comp_dropdown', 'options', allow_duplicate=True),
    Input('year_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)
def update_comp_options(year, df):
    if not year or not df:
        return []

    # Ensure df is a list of dicts
    comps = sorted({row['Competition'] for row in df if row.get('Year') == year})
    return [{'label': comp, 'value': comp} for comp in comps]

@app.callback(
    Output('age_dropdown', 'options', allow_duplicate=True),
    Input('comp_dropdown', 'value'),
    State('year_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)
def update_age_options(comp, year, df):
    if not comp or not year or not df:
        return []

    ages = sorted({row['Age Group'] for row in df 
                   if row.get('Year') == year and row.get('Competition') == comp})
    return [{'label': age, 'value': age} for age in ages]




if __name__ == '__main__':
    app.run(debug=True)