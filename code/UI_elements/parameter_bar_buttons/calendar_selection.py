import dash
from dash import Input, Output, html, dcc
import dash_mantine_components as dmc
import datetime as dt


calendar_selection = dmc.MantineProvider(

    html.Div([
        dmc.DateTimePicker(
            id='start-datetime-picker',
            placeholder='Input start date and time',
            clearable=True,
            w='auto',
            valueFormat="DD/MM/YYYY HH:mm"
        ),

        dmc.DateTimePicker(
            id='stop-datetime-picker',
            placeholder='Input stop date and time',
            clearable=True,
            w='auto',
            valueFormat="DD/MM/YYYY hh:mm"
        ),

        dcc.Store(id='calendar-time-store', data=None)

    ], style={'display': 'flex',
              'flex-wrap': 'no-wrap',
              'align-items': 'flex-end',
              'margin': '5px',
              'flex-direction': 'row',
              'column-gap': '10px'})
)


def timestamp_to_datetime(timestamp):
    timestamp = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timestamp = timestamp.replace(tzinfo=dt.timezone.utc)
    return timestamp


@dash.callback(Output(component_id='calendar-time-store', component_property='data'),
               [Input(component_id='start-datetime-picker', component_property='value'),
                Input(component_id='stop-datetime-picker', component_property='value')],
               )
def calendar_output(input_start_time, input_stop_time):
    time_dict = {'start': None, 'stop': None}
    if input_start_time:
        time_dict['start'] = timestamp_to_datetime(input_start_time)
    if input_stop_time:
        time_dict['stop'] = timestamp_to_datetime(input_stop_time)
    return time_dict
