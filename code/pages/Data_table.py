import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output

from project_functions.table_creation import create_data_table
from config.paths import MAP_POSITIONS, event_data, MAP_LOCATIONS
from project_functions.dataframe_processing import process_map_data
from UI_elements.parameter_bar import create_parameter_bar


dash.register_page(__name__, order=6)

parameter_list = ["calendar_selection", "resource_dropdown"]

columns_to_keep = ['Timestamp', 'id', 'status',  'location', 'Sublocation Name']


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

    html.Div(id='border-container', children=[
        dcc.Loading([
            html.Div(id='table-container', children=[])
        ], overlay_style={"visibility": "visible", "filter": "blur(3px)", 'opacity': 0.15})
    ], style={'border': '0px solid #73AD21'}),

], style={'position': 'relative',
          'margin-left': '12px'})


@callback(
    Output(component_id='table-container', component_property='children'),
    [
        Input(component_id='multi-resource-dropdown', component_property='value'),
        Input(component_id='calendar-time-store', component_property='data'),
    ],
    prevent_initial_call=False
)
def update_graph(id_list, time_dict):
    table = ()
    try:
        df = event_data
        df = prepare_data(df)
        df = filter_data(df, id_list, time_dict)
        df = process_map_data(df, MAP_POSITIONS, {}, MAP_LOCATIONS)
        df = df[columns_to_keep]
        table = create_data_table(df)
    except Exception as e:
        print(e)

    return table
