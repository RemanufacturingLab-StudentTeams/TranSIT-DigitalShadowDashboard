import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, _dash_renderer
import os

from UI_elements.navbar import create_navbar

_dash_renderer._set_react_version("18.2.0")

# Sets the working directory to this file, else relative paths break
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = dash.Dash(__name__,
                use_pages=True,
                pages_folder='pages',
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      dmc.styles.DATES],
                suppress_callback_exceptions=True)


app.layout = html.Div([

    dbc.Row([
        create_navbar()
    ]),

    dbc.Row([

        dbc.Container([
            dash.page_container
        ], style={'padding': '0px',
                  'margin': '0px'}
        )
    ])

], style={'padding': '0px',
          'margin': '0px',
          })


if __name__ == '__main__':
    app.run(debug=True)
