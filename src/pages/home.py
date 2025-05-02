from datetime import date, datetime, timedelta

import dash
import plotly.express as px
from dash import Input, Output, callback, dcc, html

dash.register_page(__name__, path="/")

def layout(**kwargs):
    # layout変数を定義しておくとマルチページ読み込みのときにapp.layoutに設定してくれるらしい
    fig = px.line(x=[1, 2, 3], y=[1, 2, 3])
    home_page = html.Div(
        children=[
            html.H2(children="雷検知デモ"),

            # 需給の対象エリア

            dcc.Graph(id="map-graph", figure=fig),
            dcc.Graph(id="demand-graph", figure=fig),
        ]
    )
    return home_page


# date singlepickerのdate属性をとる
@callback(
    Output("demand-graph", "figure"),
)
def update_demand_graph():

    return fig



