import dash
import pandas as pd
from dash import html, dcc, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
from PIL import Image
import time

from UI_elements.parameter_bar import create_parameter_bar
from config.paths import MAP_POSITIONS, MAP_LOCATIONS, event_data
from project_functions.dataframe_processing import process_map_data

dash.register_page(__name__, order=5)

query_range = 'start: -1h'

arrow_image_path = 'assets/arrow.png'
arrow_image = Image.open(arrow_image_path)

parameter_list = ["resource_dropdown"]

cell_style = {
    'padding': '5px',
    'border': '2px solid #dddddd',
    'font-size': '13px',
}

totals_cell_style = {
    'padding': '5px',
    'border': '2px solid #dddddd',
    'font-size': '13px',
}

important_cell_style = {
    'padding': '5px',
    'border': '2px solid #dddddd',
    'font-size': '13px',
    'font-weight': 'bold',
    'word-break': 'keep-all',
    'white-space': 'pre-line'
}


def create_comparison_table(df, resources):
    comparison_list = []
    for resource in resources:
        resource_df = df[df['id'] == resource]
        total_process, total_lead_time, process_percentage = calculate_totals(resource_df)
        total_process_str = f'{total_process}'
        total_lead_time_str = f'{total_lead_time}'
        process_percentage = f'{process_percentage} %'
        id_list = [resource, total_process_str, total_lead_time_str, process_percentage]
        comparison_list.append(id_list)
    comparison_df = pd.DataFrame(comparison_list, columns=['Resource_id',
                                                           'Total_process_time',
                                                           'Total_lead_time',
                                                           'Process_percentage'])
    data_table = html.Div([
        dash_table.DataTable(

            comparison_df.to_dict('records'), [{"name": i, "id": i} for i in comparison_df.columns],

            fixed_rows={'headers': True},

            style_table={'overflowX': 'auto',
                         'overflowY': 'auto'},

            style_cell={'minWidth': '20px',
                        'width': '40px',
                        'maxWidth': '80px',
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'padding': '5px',
                        'textAlign': 'left'},

            style_header={'backgroundColor': '#eceff0',
                          'fontWeight': 'bold',
                          'minWidth': '20px',
                          'width': '40px',
                          'maxWidth': '80px',
                          'whiteSpace': 'normal',
                          'height': 'auto'
                          },
        )
    ], style={'border-bottom': '2px solid #3f3f3f'})

    return data_table


def create_value_stream_layout(df, resource_id):
    return html.Div([

        html.H4(f'Process map for id: "{resource_id}"',
                style={'margin-bottom': '5px', 'text-decoration': 'underline'}),

        dbc.Stack(id='process-stack-container',
                  children=create_process_stack_content(df),
                  direction="horizontal",
                  gap=1,
                  style={'margin': '0px',
                         'overflow': 'auto',
                         'display': 'flex',
                         'flex-wrap': 'nowrap'}),

    ], style={'padding': '30px',
              'border-bottom': '2px solid #3f3f3f'})


def create_process_stack_content(df):
    content = []
    for index, row in df.iterrows():
        if row['is_waiting']:
            content.append(create_waiting_symbol(row))
        else:
            content.append(create_process_table(row))
    return content


def create_process_table(event):
    return html.Table([
        html.Tbody([

            html.Tr([
                html.Td('Process', style=important_cell_style),
                html.Td(event['status'], style=important_cell_style)

            ], style={'background-color': '#f5f5f5', 'border': '3px solid #73AD21'}),

            html.Tr([
                html.Td('Start time', style=cell_style),
                html.Td(str(event['Timestamp']))

            ], style=cell_style),

            html.Tr([
                html.Td('Process time', style=cell_style),
                html.Td(str(event['time_spent']))

            ], style=cell_style),

            html.Tr([
                html.Td('Sublocation Name', style=cell_style),
                html.Td(event['Sublocation Name'])

            ], style=cell_style),

        ])
    ], style={'border': '3px solid #73AD21', 'align-self': 'stretch', 'width': 'auto'})


def create_waiting_symbol(event):
    return html.Div([
        html.Img(src=arrow_image, style={'object-fit': 'contain', 'width': '80px', 'margin': '5px'}),

        html.P('Time waited:', style={'width': 'auto',
                                      'text-align': 'center',
                                      'margin': '0px',
                                      'text-decoration': 'underline',
                                      'font-size': '13px',
                                      'word-break': 'keep-all',
                                      'white-space': 'nowrap'}),

        html.P(str(event.get("time_spent")), style={'width': 'auto',
                                                    'text-align': 'center',
                                                    'margin': '0px',
                                                    'font-size': '13px',
                                                    'word-break': 'normal',
                                                    'white-space': 'nowrap'
                                                    })

    ], style={'display': 'flex',
              'justify-content': 'center',
              'padding': '5px',
              'align-content': 'center',
              'align-items': 'center',
              'flex-direction': 'column'})


def create_total_table(df):
    total_process, total_lead_time, process_percentage = calculate_totals(df)

    return html.Table([
        html.Tbody([

            html.Tr([
                html.Td('Total production process time', style=totals_cell_style),
                html.Td('Total production lead time', style=totals_cell_style),
                html.Td('Process/Lead time (%)', style=important_cell_style)
            ], style={'background-color': '#eaeaea'}),

            html.Tr([
                html.Td(str(total_process), style=totals_cell_style),
                html.Td(str(total_lead_time), style=totals_cell_style),
                html.Td(f'{process_percentage} %', style=important_cell_style)
            ], style=cell_style)

        ])
    ], style={'margin': '0px', 'border-bottom': '3px solid #73AD21'})


def calculate_totals(df):
    # ~ used to invert the filter mask
    process_df = df[~df["is_waiting"]]
    wait_df = df[df["is_waiting"]]
    total_process = process_df['time_spent'].sum()
    total_wait = wait_df['time_spent'].sum()
    lead_time = total_process + total_wait
    process_percentage = (total_process / lead_time) * 100
    rounded_percentage = round(process_percentage, 2)
    return total_process, lead_time, rounded_percentage


def prepare_data(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ns')
    df['Timestamp'] = df['Timestamp'].dt.tz_convert('UTC')
    df['id'] = df['id'].astype(str)
    return df


layout = html.Div(id='page-container', children=[

    create_parameter_bar(parameter_list),

    html.Div(id='border-container', children=[
        dcc.Loading([
            html.Div(id='comparison-container', children=[]),

            dbc.Col(id='value-stream-map-container', children=[])
        ], overlay_style={"visibility": "visible", "filter": "blur(3px)", 'opacity': 0.15})
    ], style={'border': '0px solid #73AD21',
              'padding': '0px'}),

],
                       style={'position': 'relative',
                              'padding': '0px',
                              'margin-left': '12px'})


@callback(
    [Output(component_id='value-stream-map-container', component_property='children'),
     Output(component_id='comparison-container', component_property='children')],
    Input(component_id='multi-resource-dropdown', component_property='value'),
    prevent_initial_call=True
)
def update_value_stream_map(resources):
    resources_with_data = []
    comparison_table = []
    value_stream_maps = []
    processed_df = []
    if resources is not None:
        time.sleep(0.1)
        try:
            df = event_data
            if not df.empty:
                df = prepare_data(df)
                processed_df = process_map_data(df, MAP_POSITIONS, {}, MAP_LOCATIONS)
                processed_df = processed_df.dropna()

            for resource in resources:
                resource_df = processed_df[processed_df['id'] == resource]
                if not resource_df.empty:
                    resources_with_data.append(resource)
                    vsm = create_value_stream_layout(resource_df, resource)
                    value_stream_maps.append(vsm)
                if resource_df.empty:
                    value_stream_maps.append(
                        html.H4(f'No data for id: "{resource}"',
                                style={'margin': '0px', 'text-decoration': 'underline'}),
                    )

            comparison_table = create_comparison_table(processed_df, resources_with_data)

        except Exception as e:
            print(e)

        return value_stream_maps, comparison_table
