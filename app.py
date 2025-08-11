import dash
from dash import Dash, html, dcc, no_update
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
server = app.server

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
    children= \
        [
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
            [dbc.Nav(dbc.NavItem(html.Img(src = 'assets/dance_shoes_white.png', alt = 'image', height = '40px')))]
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


# ------------------------------------------------------------
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


# ------------------------------------------------------------
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


# ------------------------------------------------------------
@app.callback(
    Output('graph', 'figure', allow_duplicate=True),
    Output('table', 'data', allow_duplicate=True),
    Output('df_chosen', 'data', allow_duplicate=True),
    Output('data_markdown', 'children', allow_duplicate=True),
    Output('table_title', 'children'),
    Output('graph_title', 'children'),
    Input('comp_submit_btn', 'n_clicks'),
    State('year_dropdown', 'value'),
    State('comp_dropdown', 'value'),
    State('age_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)
def update_table_and_graph(n_clicks, year, comp, age, df_data):
    # Early exit if button not clicked
    if n_clicks is None or n_clicks < 1:
        # return no updates (or could return empties)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Build an empty graph for fallback
    empty_graph = {
        'data': [],
        'layout': {
            'xaxis': {'showgrid': False, 'showticklabels': False, 'ticks': '', 'zeroline': False},
            'yaxis': {'showgrid': False, 'showticklabels': False, 'ticks': '', 'zeroline': False}
        }
    }

    # Validate stored data
    if not df_data:
        return empty_graph, [], [], "No data available.", "", ""

    df = pd.DataFrame(df_data)

    # Filter selection
    df_chosen = df[
        (df['Year'] == year) &
        (df['Competition'] == comp) &
        (df['Age Group'] == age)
    ]

    # If no rows match, return empty graph/table with message
    if df_chosen.empty:
        return empty_graph, [], [], "No results found for that selection.", "", ""

    # Columns to drop for plotting & table
    drop_list = ["Competition", "Year", "Age Group", "Number"]
    drop_list_for_table = ["Competition", "Year", "Age Group"]

    # Prepare data structures
    # dance_to_placings_df preserves column order and keeps Name column first if present
    dance_to_placings_df = df_chosen.drop(columns=[c for c in drop_list if c in df_chosen.columns], errors='ignore').reset_index(drop=True)

    # Ensure 'Name' is the first column used for legend labels (if exists)
    cols = dance_to_placings_df.columns.tolist()
    if 'Name' in cols and cols[0] != 'Name':
        cols = ['Name'] + [c for c in cols if c != 'Name']
        dance_to_placings_df = dance_to_placings_df[cols]

    # Columns for x axis are everything except the first (Name)
    if len(dance_to_placings_df.columns) < 2:
        # not enough columns to plot
        return empty_graph, dance_to_placings_df.to_dict('records'), dance_to_placings_df.to_dict('records'), "Not enough dance columns to plot.", "", ""

    chosen_dances = dance_to_placings_df.columns.tolist()  # preserves order

    # table data (drop only the small set)
    table_df = df_chosen.drop(columns=[c for c in drop_list_for_table if c in df_chosen.columns], errors='ignore').reset_index(drop=True)
    table_data = table_df.to_dict('records')

    # Build placings matrix (list of lists) aligned with chosen_dances
    # Convert numeric dance columns (everything except name) to floats where possible
    name_col = chosen_dances[0]
    x_cols = chosen_dances[1:]

    # Convert x columns to numeric where possible (coerce errors to NaN)
    dance_numeric = dance_to_placings_df.copy()
    for c in x_cols:
        dance_numeric[c] = pd.to_numeric(dance_numeric[c], errors='coerce')

    placings = dance_numeric[chosen_dances].values.tolist()  # rows as lists in same column order

    # Build figure traces preserving row order
    figure_data = []
    for row in placings:
        dancer_name = row[0] if row and row[0] is not None else ""  # first element is Name
        # y-values correspond to x_cols
        y_raw = row[1:]
        # Convert numpy NaN to None for Plotly compatibility
        y_vals = [None if (pd.isna(v)) else float(v) for v in y_raw]

        trace = {
            'name': str(dancer_name),
            'x': x_cols,
            'y': y_vals,
            'mode': 'lines',           # show both lines and markers
            'marker': {'symbol': 'circle', 'size': 8},
            'line': {'shape': 'linear', 'width': 10},       # you can change to 'spline' if you like
            'type': 'scatter'
        }
        figure_data.append(trace)


    graph_data = {
        'data': figure_data,
        'layout': {
            'yaxis': {'autorange': 'reversed', 'side': 'left', 'fixedrange': True},
            'xaxis': {'side': 'top', 'fixedrange': True},
            'legend': {'orientation': 'h', 'y': 0, 'yanchor': "bottom", 'yref': "container"},
            'margin': {
                # 'l': 15, 'r': 0, 
                       't': 30},
            'hovermode': 'x',   
        }
    }

    selected_data = f'Results for {year} {comp} {age}:'
    tips = (
        "**Viewing Tips:**\n\n"
        "* Turn phone sideways\n"
        "* Table Tip - Scroll left/right\n"
        "* Table Tip - Sort by clicking up/down arrows on column titles\n"
        "* Graph Tip - Click on graph points for more info\n"
        "* Graph Tip - Double click on dancer name in legend to view individual results\n"
    )
    table_title = f"**Table {selected_data}**"
    graph_title = f"**Plotted {selected_data}**"

    return graph_data, table_data, df_chosen.to_dict('records'), tips, table_title, graph_title


# ------------------------------------------------------------
@app.callback(
    Output('table', 'data', allow_duplicate=True),
    Output('graph', 'figure', allow_duplicate=True),
    Output('data_markdown', 'children', allow_duplicate=True),
    Output('year_dropdown', 'value', allow_duplicate=True),
    Output('comp_dropdown', 'value', allow_duplicate=True),
    Output('age_dropdown', 'value', allow_duplicate=True),
    Output('table_title', 'children', allow_duplicate=True),
    Output('graph_title', 'children', allow_duplicate=True),
    Input('reset_btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_outputs(n_clicks):
    if not n_clicks:
        return no_update

    empty_graph = {
        'data': [],
        'layout': {
            'xaxis': {
                'showgrid': False,
                'showticklabels': False,
                'ticks': '',
                'zeroline': False
            },
            'yaxis': {
                'showgrid': False,
                'showticklabels': False,
                'ticks': '',
                'zeroline': False
            }
        }
    }

    return [], empty_graph, ['''Please select year, competition, and age group first.'''], None, None, None, [], []

# ------------------------------------------------------------
@app.callback(
    Output('search_table', 'data', allow_duplicate=True),
    Output('search_markdown', 'children', allow_duplicate=True),
    Input('search_submit_btn', 'n_clicks'),
    State('search_name_dropdown', 'value'),
    State('df_store', 'data'),
    prevent_initial_call=True
)
def update_dancer_search(n_clicks, search_name, df_data):
    # Early exit if button not clicked
    if n_clicks is None or n_clicks < 1:
        # return no updates (or could return empties)
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    df = pd.DataFrame(df_data)

    desired_cols = ['Year',
                    'Competition',
                    'Age Group']
    undesired_cols = ['Name',
                      'Number']
    
    returned_df = df[df['Name'] == search_name]
    returned_df = returned_df.drop(undesired_cols, axis = 1)
    returned_df = returned_df[desired_cols + [col for col in list(returned_df.columns) if col not in desired_cols]].to_dict('records')
    
    return returned_df, ''
    
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)