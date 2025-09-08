import plotly.graph_objs as go

import xml.etree.ElementTree as eT
import base64


def create_graph(image_path,
                 data=None,
                 selected_scatter_mode=None,
                 multiple_traces=False,
                 status_color_map=None,
                 status_symbol_map=None
                 ):

    figure = go.Figure()

    image = encode_image(image_path)
    map_width, map_height = get_image_dimensions(image_path)
    figure = add_map_image(figure, image, map_width, map_height)

    if data is not None:
        add_data_traces(figure,
                        data,
                        selected_scatter_mode,
                        multiple_traces,
                        status_color_map,
                        status_symbol_map)

    legend_title = selected_scatter_mode['legend_title']
    figure = update_figure_layout(figure, map_width, map_height, legend_title)
    return figure


def encode_image(svg_image_path):
    with open(svg_image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image


def get_image_dimensions(svg_image_path):
    # code for getting svg size
    tree = eT.parse(svg_image_path)
    root = tree.getroot()

    width = root.get('width')
    height = root.get('height')

    if width.endswith('px'):
        width = width.replace('px', '')
    if height.endswith('px'):
        height = height.replace('px', '')

    width = float(width)
    height = float(height)

    return width, height


def add_map_image(figure, image, image_width, image_height):

    figure.add_layout_image(
        source='data:image/svg+xml;base64,{}'.format(image),
        xref="x",
        yref="y",
        x=0,
        y=0,
        sizex=image_width*1,
        sizey=image_height*1,
        sizing="fill",
        layer="below"
    )

    return figure


def add_data_traces(figure,
                    data,
                    selected_scatter_mode,
                    multiple_traces=False,
                    status_color_map=None,
                    status_symbol_map=None):

    if multiple_traces is True:
        figure = add_multiple_traces(figure,
                                     data,
                                     selected_scatter_mode,
                                     status_color_map,
                                     status_symbol_map
                                     )
    else:
        figure = add_single_trace(figure,
                                  data,
                                  selected_scatter_mode,
                                  selected_scatter_mode['marker_name'],
                                  status_color_map,
                                  status_symbol_map
                                  )
    return figure


def add_multiple_traces(figure,
                        data,
                        selected_scatter_mode,
                        status_color_map=None,
                        status_symbol_map=None):

    for row, group in data:
        figure = add_single_trace(figure, group, selected_scatter_mode, row, status_color_map, status_symbol_map)

    return figure


def add_single_trace(figure,
                     trace_data,
                     selected_scatter_mode,
                     marker_name,
                     status_color_map=None,
                     status_symbol_map=None):

    figure.add_traces([
        go.Scatter(
            x=trace_data['X_coord'],
            y=trace_data['Y_coord'],
            mode=selected_scatter_mode['mode'],
            marker=dict(
                symbol=get_marker_symbol(selected_scatter_mode, status_symbol_map, status=marker_name),
                angleref=selected_scatter_mode['angleref'],
                color=get_marker_color(selected_scatter_mode, status_color_map, status=marker_name),
                size=get_marker_size(trace_data, selected_scatter_mode),
                sizemode='diameter',
                opacity=1,

                line=dict(
                    width=2,
                    color='black'
                ),
            ),
            text=trace_data['hover_text'],
            hoverinfo='text',
            name=marker_name,
            showlegend=True
        )
    ])
    return figure


def get_marker_size(group, selected_scatter_mode):
    marker_size = group.get('marker_size', selected_scatter_mode['marker_size'])
    return marker_size


def get_marker_color(selected_scatter_mode, status_color_map=None, status=None):
    if status_color_map is None:
        marker_color = selected_scatter_mode['marker_color']
    else:
        marker_color = status_color_map[status]

    return marker_color


def get_marker_symbol(selected_scatter_mode, status_symbol_map=None, status=None):
    if status_symbol_map is None:
        marker_symbol = selected_scatter_mode['marker_symbol']
    else:
        marker_symbol = status_symbol_map[status]

    return marker_symbol


def update_figure_layout(fig, image_width, image_height, legend_title=None):
    fig.update_layout(

        xaxis=dict(
            range=[0, image_width],
            showgrid=False,
            zeroline=False,
            visible=False,
            autorange=False,
            scaleanchor="x",
            scaleratio=1,
            minallowed=0,
            maxallowed=image_width
        ),

        yaxis=dict(
            range=[image_height, 0],
            showgrid=False,
            zeroline=False,
            visible=False,
            autorange=False,
            scaleanchor="x",
            scaleratio=1,
            minallowed=0,
            maxallowed=image_height
        ),

        legend=dict(
            x=0,
            y=0,
            bgcolor="White",
            bordercolor='Black',
            borderwidth=2,
        ),

        legend_title_text=legend_title,
        uirevision='pause',
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#ffffff',
        width=image_width*1.5,
        height=image_height*1.5,
    )

    return fig
