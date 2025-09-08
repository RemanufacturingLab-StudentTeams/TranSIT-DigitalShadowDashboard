from dash import html

from UI_elements.parameter_bar_buttons.visualization_selector_analysis import visualization_dropdown_analysis
from UI_elements.parameter_bar_buttons.resource_input import resource_input
from UI_elements.parameter_bar_buttons.resource_dropdown import multi_resource_dropdown
from UI_elements.parameter_bar_buttons.calendar_selection import calendar_selection


def create_parameter_bar(parameter_list):
    return html.Div([

        html.H4('Parameters: ', style={'margin': '0px', 'color': 'black'}),

        html.Div(create_parameter_selectors(parameter_list),

                 style={'display': 'flex', 'column-gap': '10px'}),

    ], style={'display': 'flex',
              'flex-wrap': 'no-wrap',
              'align-items': 'center',
              'flex-direction': 'row',
              'column-gap': '10px',
              'padding': '6px',
              'backgroundColor': '#f0f1f1',
              'padding-left': '18px',
              'border-bottom': '3px solid #28242c',
              }
    )


def create_parameter_selectors(parameter_list):
    selector_map = {
        "visualization_dropdown_analysis": visualization_dropdown_analysis,
        "resource_input": resource_input,
        "resource_dropdown": multi_resource_dropdown,
        "calendar_selection": calendar_selection,
    }
    return [selector_map[parameter] for parameter in parameter_list]
