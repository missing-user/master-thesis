import dash
import simsopt
import simsopt.geo
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

import plotly.io as pio
import plotly.express as px
import os
import json

pio.templates.default = "plotly_dark"

import diskcache

cache = diskcache.Cache("./.cachedir")
long_callback_manager = dash.long_callback.DiskcacheLongCallbackManager(cache)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    long_callback_manager=long_callback_manager,
)

out_dir = "output"
directories = [
    os.path.join(out_dir, name)
    for name in os.listdir(out_dir)
    if os.path.isdir(os.path.join(out_dir, name))
]
all_paths = list(reversed(sorted(directories)))

app.layout = dash.html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dash.dcc.Dropdown(
                            options=all_paths, value=all_paths[0], id="fileselect"
                        ),
                        dash.dcc.Dropdown(id="scalarselect"),
                    ]
                ),
                dbc.Col(
                    [
                        dash.html.Label("Success Threshold"),
                        dash.dcc.Slider(0, 1, 0.05, value=0.5, id="threshold-slider"),
                    ]
                ),
            ]
        ),
        dbc.Row(dash.html.Progress(id="progress_bar")),
        dbc.Row(
            [
                dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="figure1", figure={}))),
                dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="hover_fig", figure={}))),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="BdotN", figure={}))),
                dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="Btarget", figure={}))),
                # dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="BdotNfft", figure={}))),
                dbc.Col(dash.dcc.Loading(dash.dcc.Graph(id="Btargetfft", figure={}))),
            ]
        ),
        dash.dcc.Store(id="df-store"),
    ],
    **{"data-bs-theme": "dark"},
)

from skimage.filters import window
import matplotlib.pyplot as plt


def spectral_radius(Bn):
    Bn = np.array(Bn)
    # lambda x: np.sum(np.abs(np.fft.fft2(x).imag))
    w = 1.0 - window(25, (min(Bn.shape), min(Bn.shape)))
    center_x = (Bn.shape[0] - w.shape[0]) // 2
    center_y = (Bn.shape[1] - w.shape[1]) // 2
    w_padded = np.ones_like(Bn)
    w_padded[center_x : center_x + w.shape[0], center_y : center_y + w.shape[1]] = w
    fftImg = np.fft.fft2(Bn)
    windowedImg = np.fft.fftshift(w_padded) * np.abs(fftImg)
    # plt.subplot(131)
    # plt.imshow(np.fft.fftshift(windowedImg))
    # plt.subplot(132)
    # plt.imshow(np.fft.fftshift(np.abs(fftImg)))
    # plt.subplot(133)
    # plt.imshow(np.abs(w_padded))
    # plt.show()

    return np.mean(windowedImg)


def spectral_radius2(Bn):
    Bn = np.array(Bn)
    # lambda x: np.sum(np.abs(np.fft.fft2(x).imag))
    w_padded = np.ones_like(Bn) * 0.02
    w = window(25, (min(Bn.shape), min(Bn.shape)))
    center_x = (Bn.shape[0] - w.shape[0]) // 2
    center_y = (Bn.shape[1] - w.shape[1]) // 2
    w_padded[center_x : center_x + w.shape[0], center_y : center_y + w.shape[1]] += w
    fftImg = np.fft.fft2(Bn)
    windowedImg = np.abs(fftImg) / np.fft.fftshift(w_padded)
    # plt.subplot(131)
    # plt.imshow(np.fft.fftshift(windowedImg))
    # plt.subplot(132)
    # plt.imshow(np.fft.fftshift(np.abs(fftImg)))
    # plt.subplot(133)
    # plt.imshow(np.abs(w_padded))
    # plt.show()

    return np.mean(windowedImg)


@app.long_callback(
    dash.Output("df-store", "data"),
    dash.Input("fileselect", "value"),
    running=[
        (
            dash.Output("progress_bar", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        )
    ],
    manager=long_callback_manager,
    progress=[dash.Output("progress_bar", "value"), dash.Output("progress_bar", "max")],
)
def load_results(set_progress, filepath):
    analysis_folder = os.path.join(filepath)
    results = []
    i = 0
    all_files = os.listdir(analysis_folder)
    for i, path in enumerate(all_files):
        if path.endswith(".json"):
            # optimization_res = simsopt.load(analysis_folder + "/" + path)
            with open(analysis_folder + "/" + path) as f:
                optimization_res_sopt = json.load(f)
                optimization_res = {}
                for key in optimization_res_sopt["graph"]:
                    if isinstance(optimization_res_sopt["graph"][key], dict):
                        if "@module" in optimization_res_sopt["graph"][key]:
                            optimization_res[key] = optimization_res_sopt["graph"][key][
                                "data"
                            ]
                    else:
                        optimization_res[key] = optimization_res_sopt["graph"][key]
            optimization_res["filename"] = str(path)
            results.append(optimization_res)

        set_progress((str(i + 1), str(len(all_files))))

    df = pd.DataFrame(results).convert_dtypes()
    df["J"] = df["J"].astype(float)
    df["B target max"] = df["B_external_normal"].apply(np.max)
    df["B.n residual max"] = df["BdotN"].apply(np.max)
    df["spectral_power_post"] = df["B_external_normal"].apply(spectral_radius)
    df["spectral_power2_post"] = df["B_external_normal"].apply(spectral_radius2)
    df["energy"] = df["B_external_normal"].apply(
        lambda x: np.sum(np.abs(np.fft.fft2(x).imag))
    )
    df["spectral_radius"] = df["spectral_radius"].astype(float)
    df["complexity"] = df["complexity"].astype(float)
    df["magnitude"] = df["magnitude"].astype(float)
    return df.select_dtypes(exclude=["object"]).to_dict("records")


@app.callback(dash.Output("scalarselect", "options"), dash.Input("df-store", "data"))
def dropdown(dfstore):
    df = pd.DataFrame(dfstore).convert_dtypes()
    return df.select_dtypes(include=["number"]).columns.tolist()


@app.callback(
    dash.Output("figure1", "figure"),
    dash.Input("df-store", "data"),
    dash.Input("threshold-slider", "value"),
    dash.Input("scalarselect", "value"),
)
def scatterplot(dfstore, success_threshold, xscalar):
    df = pd.DataFrame(dfstore).convert_dtypes()
    df["max residual to target ratio"] = df["B.n residual max"] / df["B target max"]

    fig = px.scatter(
        df[df["max residual to target ratio"] <= success_threshold],
        xscalar,
        "complexity",
        color="max residual to target ratio",
        range_color=[0, 1],
        hover_data={"filename": True},
    )
    return fig.update_layout(clickmode="event", height=600)


@app.callback(
    dash.Output("BdotN", "figure"),
    dash.Output("Btarget", "figure"),
    # dash.Output("BdotNfft", "figure"),
    dash.Output("Btargetfft", "figure"),
    dash.Input("figure1", "hoverData"),
    dash.Input("fileselect", "value"),
)
def display_hover_data1(hoverData, filepath):
    if not hoverData or not filepath:
        return {}, {}, {}

    result_path = str(hoverData["points"][0]["customdata"][0])
    optimization_res = simsopt.load(os.path.join(filepath, result_path))

    targetmin, targetmax = np.min(optimization_res["B_external_normal"]), np.max(
        optimization_res["B_external_normal"]
    )
    extnorm = optimization_res["B_external_normal"]
    return (
        # px.imshow(
        #     optimization_res["BdotN"],
        #     title="B.n residual",
        #     range_color=[targetmin, targetmax],
        # ),
        px.imshow(
            np.fft.fftshift(np.fft.fft2(optimization_res["BdotN"])).imag,
            title="B.n residual",
            # range_color=[targetmin, targetmax],
        ),
        px.imshow(
            extnorm,
            title=f"B.n target ({result_path})",
        ),
        px.imshow(
            np.fft.fftshift(np.fft.fft2(extnorm)).imag,
            title="B.n target FFT",
            x=np.fft.fftshift(
                np.fft.fftfreq(extnorm.shape[1], d=1.0 / extnorm.shape[1])
            ),
            y=np.fft.fftshift(
                np.fft.fftfreq(extnorm.shape[0], d=1.0 / extnorm.shape[0])
            ),
        ),
    )


@app.callback(
    dash.Output("hover_fig", "figure"),
    dash.Input("figure1", "clickData"),
    dash.State("fileselect", "value"),
)
def display_hover_data(hoverData, filepath):
    if not hoverData or not filepath:
        return {}

    result_path = str(hoverData["points"][0]["customdata"][0])
    optimization_res = simsopt.load(os.path.join(filepath, result_path))

    return simsopt.geo.plot(
        [optimization_res["surf"]] + optimization_res["coils"],
        show=False,
        engine="plotly",
        close=True,
    ).update_layout(height=600, title=result_path)


app.run(debug=True, port=8052)
