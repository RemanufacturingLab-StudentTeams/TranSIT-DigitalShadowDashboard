import dash
from dash import html, dcc

from config.paths import IMAGE_PATH, MAP_POSITIONS
from config.scatter_graph_config import graph_config, scatter_modes
from project_functions.graph_creation import create_graph

dash.register_page(__name__, order=3)

FLOORPLAN = IMAGE_PATH
LOCATIONS_DATA = MAP_POSITIONS
SELECTED_MODE = scatter_modes['locations']


def create_locations_map(image, df, mode):
    df = df.pipe(add_hover_text)
    figure = create_graph(image, data=df, selected_scatter_mode=mode,)
    return figure


def add_hover_text(df):

    df['hover_text'] = df.apply(

        lambda row: f"ID: {row['id']}<br>"
                    f"Name: {row['name']}<br>"
                    f"Department: {row['department']}<br>"
                    f"X coordinate on floorplan: {row['X_coord']}<br>"
                    f"Y coordinate on floorplan: {row['Y_coord']}<br>"
                    f"Associated statuses: {row['associated_status']}"
                    , axis=1
    )
    return df


layout = html.Div(id='page-container', children=[

    html.Div([

        html.Div(id='graph-container', children=[
            dcc.Loading([
                dcc.Graph(id='locations-map',
                          figure=create_locations_map(FLOORPLAN, LOCATIONS_DATA, SELECTED_MODE),
                          config=graph_config)

            ], overlay_style={"visibility": "visible", "filter": "blur(3px)", 'opacity': 0.15})
        ], style={'padding': '60px', 'padding-top': '20px'}),
    ],
        id='flex-box',
        style={'display': 'flex',
               'justify-content': 'center',
               'align-self': 'flex-end'}
    )

], style={'position': 'relative',
          'margin-left': '12px'})
