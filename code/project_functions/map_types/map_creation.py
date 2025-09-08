from project_functions.graph_creation import create_graph
from project_functions.dataframe_processing import process_map_data
from project_functions.map_types.averages_graph import create_averages_graph

from config.scatter_graph_config import scatter_modes
from config.paths import IMAGE_PATH, MAP_POSITIONS, MAP_LOCATIONS


def create_concentration_map(query_df, selected_scatter_mode):
    figure_data = process_map_data(query_df, MAP_POSITIONS, selected_scatter_mode, MAP_LOCATIONS)
    figure = create_graph(IMAGE_PATH,
                          data=figure_data,
                          selected_scatter_mode=selected_scatter_mode)
    return figure


def create_route_map(query_df, selected_scatter_mode):
    figure_data = process_map_data(query_df, MAP_POSITIONS, selected_scatter_mode, MAP_LOCATIONS)
    figure = create_graph(IMAGE_PATH,
                          data=figure_data,
                          selected_scatter_mode=selected_scatter_mode,
                          multiple_traces=True)
    return figure


def create_averages_map(query_df, selected_scatter_mode):
    figure_data = process_map_data(query_df, MAP_POSITIONS, selected_scatter_mode, MAP_LOCATIONS)
    figure = create_averages_graph(IMAGE_PATH, figure_data, selected_scatter_mode)
    return figure


def create_blank_map():
    figure = create_graph(IMAGE_PATH, selected_scatter_mode=scatter_modes['overview'])
    return figure
