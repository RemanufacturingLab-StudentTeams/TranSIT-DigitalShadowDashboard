import dash
from dash import callback_context as ctx
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc


visualization_options = [
    dbc.DropdownMenuItem('Concentration', id='concentration-item'),
    dbc.DropdownMenuItem('Part routes', id='part-item'),
    dbc.DropdownMenuItem('Average times', id='averages-item'),
]

visualization_dropdown_analysis = html.Div([
    dbc.DropdownMenu(
        visualization_options,
        id='visualization-dropdown-analysis',
        label='Visualization type: "routes"',
        color='primary',
        menu_variant='dark'
    ),
    dcc.Store(data='routes', id='visualization-store-analysis')
], style={"display": "flex", "align-items": "center"})


@dash.callback(
    [Output('visualization-dropdown-analysis', 'label'),
     Output('visualization-store-analysis', 'data')],
    [Input('concentration-item', 'n_clicks'),
     Input('part-item', 'n_clicks'),
     Input('averages-item', 'n_clicks')],
    prevent_initial_call=True,
)
def update_visualization_button(o_clicks, c_clicks, p_clicks):
    # using code online for determining which input was clicked via ctx
    if not ctx.triggered:
        return dash.no_update
    item_id = ctx.triggered[0]['prop_id'].split('.')[0]

    clicks_visualization_map = {
        'overview-item': 'overview',
        'concentration-item': 'concentration',
        'part-item': 'routes',
        'averages-item': 'average times',
    }
    visualization_type = clicks_visualization_map.get(item_id)
    return f'Visualization type: "{visualization_type}"', visualization_type
