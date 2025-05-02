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
                html.H1("電力需給・電力市場DashBoard"),
                width=12,
                style={"background-color": "palegreen", "color": "white"},
            )
        ),
        dbc.Row(
            [dbc.Col(dash.page_container, width=12)],
            style={"height": "90vh"},
        ),
    ],
    fluid=True,
)