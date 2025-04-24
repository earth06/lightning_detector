import numpy as np
import pandas as pd


def get_M(a, b):
    m = (a + b) / 2.0
    return m


def shift_to_O(a, m):
    a0 = a - m
    return a0


def calc_rot_gamma(a, b):
    gamma = np.arctan(-(a[1] - b[1]) / (a[0] - b[0]))
    return gamma


def rotation(gamma, X0):
    rot_x = X0[0] * np.cos(gamma) - X0[1] * np.sin(gamma)
    rot_y = X0[0] * np.sin(gamma) + X0[1] * np.cos(gamma)
    rotX = np.array((rot_x, rot_y))
    return rotX


# 頂点alphaを求める(本来ここは観測で得られるものだが一旦ダミーなので)
def calc_alpha(rot_a, rot_b, rot_lt):
    alpha = 0.5 * (
        np.sqrt((rot_a[0] - rot_lt[0]) ** 2 + (rot_a[1] - rot_lt[1]) ** 2)
        - np.sqrt((rot_b[0] - rot_lt[0]) ** 2 + (rot_b[1] - rot_lt[1]) ** 2)
    )
    return alpha


def calc_alpha_from_delat_t(delta_t):
    c = 3.0e8
    return 0.5 * c * delta_t


def calc_beta(rot_a, alpha):
    beta = np.abs(np.abs(rot_a[0]) ** 2 - alpha**2) ** 0.5
    return beta


def generate_hyper(alpha, beta):
    x_minus = np.linspace(-20, -np.abs(alpha), 800)
    x_plus = np.linspace(np.abs(alpha), 20.1, 800)
    y_1 = (beta / alpha) * np.sqrt(x_plus**2 - alpha**2)
    y_2 = (beta / alpha) * np.sqrt(x_minus**2 - alpha**2)
    y_3 = (-beta / alpha) * np.sqrt(x_minus**2 - alpha**2)
    y_4 = (-beta / alpha) * np.sqrt(x_plus**2 - alpha**2)
    return (x_plus, y_1), (x_minus, y_2), (x_minus, y_3), (x_plus, y_4)


def rotation_vector(gamma, X, Y):
    X_rot = X * np.cos(gamma) - Y * np.sin(gamma)
    Y_rot = X * np.sin(gamma) + Y * np.cos(gamma)
    return X_rot, Y_rot


def shift_vector(X, Y, m):
    X_shift = X + m[0]
    Y_shift = Y + m[1]
    return X_shift, Y_shift


def generate_lightning():
    lon = np.random.uniform(low=132, high=140, size=1)
    lat = np.random.uniform(
        low=33,
        high=39,
        size=1,
    )
    return (lon, lat)


def calculate_arrival_time(df, lightning_lon, lightning_lat):
    c = 3.0e8
    arrive_times = (
        np.sqrt((df["lon"] - lightning_lon) ** 2 + (df["lat"] - lightning_lat) ** 2) / c
    )
    return arrive_times


def decide_lightning_hyperbola(a, b, delta_t):
    # 中点を求める
    m = get_M(a, b)
    # abの中点が原点になるように平行移動
    a0 = shift_to_O(a, m)
    b0 = shift_to_O(b, m)
    print(a0, b0)

    # 焦点のy座標が０になるように回転させる
    gamma = calc_rot_gamma(a0, b0)
    rot_a = rotation(gamma, a0)
    rot_b = rotation(gamma, b0)
    print(rot_a, rot_b)

    # 双曲線のパラメータを求める
    alpha = calc_alpha_from_delat_t(delta_t)
    beta = calc_beta(rot_a, alpha)
    print(alpha, beta)

    # 双曲線配列を生成
    z1, z2, z3, z4 = generate_hyper(alpha, beta)

    # 双曲線を元の位置に回転する
    z1_rot = rotation_vector(-gamma, z1[0], z1[1])
    z2_rot = rotation_vector(-gamma, z2[0], z2[1])
    z3_rot = rotation_vector(-gamma, z3[0], z3[1])
    z4_rot = rotation_vector(-gamma, z4[0], z4[1])

    # 双曲線を元の位置に平行移動する
    z1_shift = shift_vector(z1_rot[0], z1_rot[1], m)
    z2_shift = shift_vector(z2_rot[0], z2_rot[1], m)
    z3_shift = shift_vector(z3_rot[0], z3_rot[1], m)
    z4_shift = shift_vector(z4_rot[0], z4_rot[1], m)

    return (z1_shift, z2_shift, z3_shift, z4_shift)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs

    df = pd.read_csv("../src/lightning_obs_station.csv")
    lt_lon, lt_lat = generate_lightning()
    df["arrive_time"] = calculate_arrival_time(df, lt_lon, lt_lat)
    df_sort = df.sort_values("arrive_time").head(4).reset_index(drop=True)
    k = df_sort.iloc[0][["lon", "lat"]].to_numpy()
    l = df_sort.iloc[1][["lon", "lat"]].to_numpy()
    m = df_sort.iloc[2][["lon", "lat"]].to_numpy()
    n = df_sort.iloc[3][["lon", "lat"]].to_numpy()

    z_lm = decide_lightning_hyperbola(
        l, m, np.abs(df_sort.iloc[1]["arrive_time"] - df_sort.iloc[2]["arrive_time"])
    )
    z_mn = decide_lightning_hyperbola(
        m, n, np.abs(df_sort.iloc[2]["arrive_time"] - df_sort.iloc[3]["arrive_time"])
    )

    z_kl = decide_lightning_hyperbola(
        k, l, np.abs(df_sort.iloc[0]["arrive_time"] - df_sort.iloc[1]["arrive_time"])
    )

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(
        1,
        1,
        1,
        projection=ccrs.AzimuthalEquidistant(
            central_longitude=135, central_latitude=35
        ),
    )
    ax.gridlines(draw_labels=True)
    ax.coastlines()
    ax.set_extent([132, 140, 33, 39], ccrs.PlateCarree())
    for lat, lon in zip(df["lat"], df["lon"]):
        ax.plot(lon, lat, marker="o", transform=ccrs.PlateCarree(), c="gray")

    # 同定に使った観測点
    for pt in (k, l, m, n):
        ax.plot(*pt, marker="o", c="r", transform=ccrs.PlateCarree())

    # 双曲線
    for z in z_lm:
        ax.plot(*z, c="C0", transform=ccrs.PlateCarree())
    for z in z_mn:
        ax.plot(*z, c="C1", transform=ccrs.PlateCarree())
    for z in z_kl:
        ax.plot(*z, c="C2", transform=ccrs.PlateCarree())

    # 落雷位置
    ax.plot(lt_lon, lt_lat, marker="x", c="k", transform=ccrs.PlateCarree())
