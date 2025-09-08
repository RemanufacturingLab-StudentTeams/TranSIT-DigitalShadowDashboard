# These are dictionaries for the different graph options

scatter_modes = {
    'tag mapping': {
                'mode': 'markers',
                'marker_symbol': 'circle',
                'angleref': 'up',
                'marker_size': 16,
                'marker_color': '#ffc900',
                'trace': 'single',
                'hover_text_type': 'tag mapping',
                'legend_title': 'ID tagged at location',
                'marker_name':
                    'ID tagged at location'
                },

    'locations': {
            'mode': 'markers',
            'marker_symbol': 'square',
            'angleref': 'up',
            'marker_size': 16,
            'marker_color': '#ffc900',
            'trace': 'single',
            'hover_text_type': 'locations',
            'legend_title': 'Sub-locations',
            'marker_name':
                'Sub-location contains data'
            },

    'routes': {
        'mode': 'markers+lines',
        'marker_symbol': 'arrow',
        'angleref': 'previous',
        'marker_size': 16,
        'marker_color': None,
        'trace': 'groups',
        'marker_name': None,
        'hover_text_type': 'single',
        'legend_title': 'Part ID',
        'group_by': 'id'
        },

    'part routes': {
            'mode': 'markers+lines',
            'marker_symbol': 'arrow',
            'angleref': 'previous',
            'marker_size': 16,
            'marker_color': None,
            'trace': 'groups',
            'marker_name': None,
            'hover_text_type': 'single',
            'legend_title': 'data type',
            },

    'average times': {
        'mode': 'markers',
        'marker_symbol': 'square',
        'angleref': 'up',
        'marker_size': 16,
        'marker_color': '#64ff00',
        'trace': 'single',
        'hover_text_type': 'averages',
        'legend_title': 'Work station',
        'calculate_averages': True,
        'marker_name':
            'Station was active'
    },

    'concentration': {
        'mode': 'markers',
        'marker_symbol': 'circle',
        'angleref': 'up',
        'marker_size': None,
        'marker_color': '#ffc900',
        'trace': 'single',
        'hover_text_type': 'many',
        'legend_title': 'Work station',
        'marker_name':
            'Parts present<br>at location'
    },

    'overview': {
        'mode': 'markers',
        'angleref': 'up',
        'marker_size': 28,
        'filter_by': 'Status',
        'group_by': 'Status',
        'important_statuses': ('Interrupted', 'Emergency', 'Idle'),
        'trace': 'groups',
        'marker_name': 'Status',
        'hover_text_type': 'status',
        'legend_title': 'Reported statuses',

        'status_symbols': {

            'Interrupted': 'triangle-down',
            'Idle': 'triangle-down',
            'Running': 'circle',
            'Not Scheduled': 'circle',
            'Emergency': 'octagon'
        },
        'status_colors': {

            'Interrupted': '#ff5500',
            'Idle': '#ffde00',
            'Running': '#a8ff00',
            'Not Scheduled': '#00f6ff',
            'Emergency': '#ff1e00'
        },
    }
}

graph_config = {

    'scrollZoom': False,
    'modeBarButtonsToRemove': ['lasso2d', 'zoomIn', 'zoomOut', 'autoScale'],
    'showAxisDragHandles': False,
    'showAxisRangeEntryBoxes': False,
    'displaylogo': False,
    'responsive': False,

}
