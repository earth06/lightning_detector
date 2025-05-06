import dash
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

from lightning_hyperbola import LightningHyperbola

dash.register_page(__name__, path="/")

HOST = "localhost"
PORT = 18889


def layout(**kwargs):
    # layout変数を定義しておくとマルチページ読み込みのときにapp.layoutに設定してくれるらしい
    fig = px.line(x=[1, 2, 3], y=[1, 2, 3])
    home_page = html.Div(
        children=[
            html.H2(children="雷検知デモ"),
            # 需給の対象エリア
            dcc.Graph(id="map-graph", figure=update_demand_graph()),
        ]
    )
    return home_page


# # date singlepickerのdate属性をとる
# @callback(
#     Output("map-graph", "figure"),
# )
def update_demand_graph():
    colors = ["dodgerblue", "tomato", "gray"]
    lightning = LightningHyperbola()
    lightning.load_station()
    hyperbolas = lightning.get_hyperbola()
    fig = go.Figure()
    # 双曲線
    for z_s, color in zip(hyperbolas["hyperbola"], colors, strict=False):
        for z in z_s:
            fig.add_trace(go.Scattermap(mode="lines", lon=z[0], lat=z[1], marker={"color": color}))

    # 落雷地点
    fig.add_trace(
        go.Scattermap(
            mode="markers",
            lon=hyperbolas["lightning_point"][0],
            lat=hyperbolas["lightning_point"][1],
            marker={"color": "black", "size": 12, "symbol": ["cross"]},
        )
    )

    # LLS地点
    fig.add_trace(
        go.Scattermap(
            mode="markers",
            lon=lightning.station_master["lon"],
            lat=lightning.station_master["lat"],
            marker={"color": "darksalmon", "size": 14},
        )
    )

    # 評定に使ったLLS
    fig.add_trace(
        go.Scattermap(
            mode="markers",
            lon=hyperbolas["use_station"]["lon"],
            lat=hyperbolas["use_station"]["lat"],
            marker={"color": "red", "size": 14},
        )
    )
    fig.update_layout(
        map_style="white-bg",
        map_layers=[
            {"below": "traces", "sourcetype": "raster", "source": ["http://" + f"{HOST}:{PORT}" + "/{z}/{x}/{y}.png"]}
        ],
        map_zoom=6,
        map_center_lat=35,
        map_center_lon=138,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=800,
    )
    return fig
