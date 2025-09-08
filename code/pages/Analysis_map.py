import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output

from config.scatter_graph_config import graph_config, scatter_modes
from UI_elements.parameter_bar import create_parameter_bar
from config.paths import event_data
from project_functions.map_types.map_creation import (create_blank_map,
                                                      create_route_map,
                                                      create_concentration_map,
                                                      create_averages_map)


dash.register_page(__name__, order=1, path='/')

parameter_list = ["visualization_dropdown_analysis",
                  "calendar_selection",
                  "resource_dropdown"]


def prepare_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ns')
    df['Timestamp'] = df['Timestamp'].dt.tz_convert('UTC')
    df['id'] = df['id'].astype(str)
    return df


def filter_data(df, id_list, time_dict):
    if id_list:
        df = df.loc[lambda row: row['id'].isin(id_list)]
    if time_dict['start']:
        df = df.loc[lambda row: time_dict['start'] <= row['Timestamp']]
    if time_dict['stop']:
        df = df.loc[lambda row: time_dict['stop'] >= row['Timestamp']]
    return df


layout = html.Div(id='page-container', children=[

    create_parameter_bar(parameter_list),

    html.Div([], id='parameter-input-container'),

    html.Div(id='graph-container', children=[
        dcc.Loading([
            dcc.Graph(id='analysis-map-async',
                      figure=create_blank_map(),
                      config=graph_config,
                      style={'border': '0px solid #73AD21'})

        ], overlay_style={"visibility": "visible", "filter": "blur(3px)", 'opacity': 0.15})
    ], style={'padding': '60px', 'padding-top': '20px'}),

    dcc.Interval(id='interval-component', interval=60*10000)

], style={'position': 'relative',
          'margin-left': '12px'})


@callback(
    Output(component_id='analysis-map-async', component_property='figure'),
    [
        Input(component_id='visualization-store-analysis', component_property='data'),
        Input(component_id='multi-resource-dropdown', component_property='value'),
        Input(component_id='calendar-time-store', component_property='data'),
    ],
    prevent_initial_call=False
)
def update_graph(visualization_type, id_list, time_dict):
    visualization_type_graph_map = {
        'concentration': create_concentration_map,
        'routes': create_route_map,
        'average times': create_averages_map,
    }
    figure = create_blank_map()
    try:
        df = event_data
        df = prepare_data(df)
        df = filter_data(df, id_list, time_dict)
        selected_scatter_mode = scatter_modes[visualization_type]
        figure = visualization_type_graph_map[visualization_type](df, selected_scatter_mode)
    except Exception as e:
        print(e)

    return figure
