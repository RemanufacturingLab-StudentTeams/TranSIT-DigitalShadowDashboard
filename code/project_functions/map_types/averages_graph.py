from project_functions.graph_creation import *
import plotly.graph_objects as go


def create_averages_graph(image_path, data, selected_scatter_mode):
    figure = go.Figure()

    image = encode_image(image_path)
    map_width, map_height = get_image_dimensions(image_path)
    figure = add_map_image(figure, image, map_width, map_height)
    if data is not None:
        figure = add_initial_trace(figure,
                                   data,
                                   selected_scatter_mode,
                                   selected_scatter_mode.get('marker_name'))
    legend_title = selected_scatter_mode['legend_title']
    figure = update_averages_figure(figure, map_width, map_height, legend_title)
    return figure


def add_initial_trace(figure,
                      trace_data,
                      selected_scatter_mode,
                      marker_name,
                      status_symbol_map=None):

    figure.add_traces([
        go.Scatter(
            x=(trace_data['X_coord']),
            y=(trace_data['Y_coord']),
            mode=selected_scatter_mode['mode'],
            marker=dict(
                symbol=get_marker_symbol(selected_scatter_mode, status_symbol_map, status=marker_name),
                angleref=selected_scatter_mode['angleref'],
                color=trace_data['average_in_hours'],
                size=get_marker_size(trace_data, selected_scatter_mode),
                sizemode='diameter',
                opacity=1,
                reversescale=False,
                colorscale='ylorrd',
                colorbar=dict(
                    title=dict(
                        text="Average time <br>spent at <br>sub-location <br>(hours)",
                        side="top",
                    ),
                    len=0.8,
                    x=0,
                    y=1,
                    yanchor='top',
                    bgcolor='rgba(0,0,0,0)',
                    bordercolor='rgba(0,0,0,0)',
                    borderwidth=5,
                ),

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


def update_averages_figure(fig, image_width, image_height, legend_title=None):

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
        plot_bgcolor='rgba(0,0,0,0)',
        width=image_width*1.5,
        height=image_height*1.5,
    )

    return fig
