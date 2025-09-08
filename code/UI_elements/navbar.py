import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

navbar_style = {
    'margin': '0px',
    'padding': '0px'
}

link_style = {
    'color': 'white',
    'margin': '5px'
}

text_style = {
    'padding': '0px',
    'margin': '0px'
}


def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col([
                        dcc.Markdown('# Factory digital shadow',
                                     style={
                                         'text-decoration': 'underline',
                                         'color': 'white'
                                     }),
                    ], width='auto'),
                    dbc.Col([
                        dbc.Nav([
                            dbc.Stack(create_nav_links(),
                                      direction="horizontal",
                                      gap=1
                                      )
                            ],
                            style=navbar_style,
                            pills=True
                        )
                    ], width='auto')
                ],
                justify='between',
                align='center',
            ),
            style={'padding': '10px',
                   'padding-left': '30px'},
            fluid=True,
        ),
        className='navbar bg-dark',
        style={}
    )


def create_nav():
    return dbc.Nav(
        create_nav_links(),
        style=navbar_style,
        className='bg-dark',  # Uses dbc class with black background
        pills=True
    )


def create_nav_links():
    return [
        dbc.NavLink(
            [
                html.H4(page["name"],
                        style=text_style),
            ],
            style=link_style,
            href=page["path"],  # Sets url path from dash page dictionary
            active='exact',  # Needs exact url to
        )
        for page in dash.page_registry.values()  # for each page in dash page registry
    ]
