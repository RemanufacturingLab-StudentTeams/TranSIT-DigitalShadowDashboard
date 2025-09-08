import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


resource_input = html.Div([
    dbc.Input(id="resource-input", type="text", placeholder="Input a resource ID"),
    dcc.Store(data=None, id='resource-store-analysis')
    ], style={"display": "flex", "align-items": "center", 'margin': '5px'})


@dash.callback(
    Output("resource-store-analysis", "data"),
    Input("resource-input", "value"),
)
def update_resource(resource):
    if resource:
        return resource
    else:
        return None
