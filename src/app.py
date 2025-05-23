import argparse

import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html

external_stylesheets = [dbc.themes.FLATLY]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
server = app.server

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("雷鳴神"),
                width=12,
                style={"background-color": "slateblue", "color": "white"},
            )
        ),
        dbc.Row(
            [dbc.Col(dash.page_container, width=12)],
            style={"height": "95vh"},
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost", help="server's IP, ex) 100.66.1.13")
    parser.add_argument("--port", default=18889)
    args = parser.parse_args()
    # app.run(host="localhost", port=18889, debug=True)
    app.run(host=args.host, port=args.port, debug=True)
