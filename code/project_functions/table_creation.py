from dash import dash_table


def create_data_table(df):
    data_table = dash_table.DataTable(

        df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],

        fixed_rows={'headers': True},

        style_table={'overflowX': 'auto',
                     'overflowY': 'auto'},

        style_cell={'minWidth': '100px',
                    'maxWidth': '200px',
                    'whiteSpace': 'normal',
                    'height': 'auto'},

        style_header={'backgroundColor': '#eceff0',
                      'fontWeight': 'bold'}
    )

    return data_table
