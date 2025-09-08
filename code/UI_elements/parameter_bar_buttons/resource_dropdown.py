import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from config.paths import event_data


def get_id_list(df):
    id_df = df['id'].astype(str)
    id_list = id_df.tolist()
    id_list = list(set(id_list))  # Removes duplicate IDs
    return id_list


multi_resource_dropdown = html.Div([
        dcc.Dropdown(id="multi-resource-dropdown", multi=True, closeOnSelect=False, placeholder="Input a resource ID",
                     style={"width": "400px",
                            "background-color": "#FFFFFF",
                            "border-radius": "4px"},
                     ),
], style={"display": "flex", "align-items": "center", 'margin': '5px'})


@dash.callback(
    Output("multi-resource-dropdown", "options"),
    Input("multi-resource-dropdown", "search_value"),
    State("multi-resource-dropdown", "value")
)
def update_multi_options(search_value, value):
    if not search_value:
        return dash.no_update

    items_list = get_id_list(event_data)
    return items_list
