from dash import Input, Output, State, exceptions, no_update
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stat
from nor_view import app
from nor_model import stat_colours


@app.callback(
    Output("normal-dist-fig", "figure"),
    Output("z1", "invalid"),
    Output("z2", "invalid"),
    Output("error", "children"),
    Output("output", "style"),
    Output("current-mu", "children"),
    Output("current-sigma", "children"),
    Output("probability", "children"),
    Output("sr-norm", "children"),
    Input("submit", "n_clicks"),
    State("mu", "value"),
    State("sigma", "value"),
    State("calc-type", "value"),
    State("z1", "value"),
    State("z2", "value"),
    prevent_initial_call=True
)
def update_graph(n_clicks, mu, sigma, calc_type, z1, z2):
    if n_clicks is None or mu is None or sigma is None:
        raise exceptions.PreventUpdate
    else:
        x = np.linspace(stat.norm(mu, sigma).ppf(0.0001),
                        stat.norm(mu, sigma).ppf(0.9999),
                        10000)
        norm_x = stat.norm(mu, sigma).pdf(x)
        fig = go.Figure(
            go.Scatter(x=x,
                       y=norm_x,
                       marker_color=stat_colours["norm"],
                       name="Normal distribution",
                       hoverinfo="skip"),
            layout={"margin": dict(t=20, b=10, l=20, r=20),
                    "height": 400,
                    "font_size": 14})
        if calc_type == "<" or calc_type == ">":
            if z1 is None:
                return fig, True, False, "Enter a value for z1", no_update, "", "", "", ""
            else:
                sr_norm = f"Normal distribution graph with mean {mu}, standard deviation {sigma} and z1 = {z1}"
                x1 = stat.norm(mu, sigma).cdf(z1)
                if calc_type == "<":
                    probability = round(x1*100, 2)
                    prob_less_than_x1 = np.linspace(
                        stat.norm(mu, sigma).ppf(0.0001),
                        stat.norm(mu, sigma).ppf(x1),
                        10000)
                    norm_pdf = stat.norm(mu, sigma).pdf(prob_less_than_x1)
                    fig.add_trace(
                        go.Scatter(x=prob_less_than_x1,
                                   y=norm_pdf,
                                   name="Probability",
                                   marker_color=stat_colours["norm"],
                                   fill="tozeroy",
                                   fillcolor=stat_colours["z"],
                                   hoveron="fills"))
                    empirical_rule(fig, mu, sigma, norm_x)
                elif calc_type == ">":
                    probability = round((1 - x1)*100, 2)
                    prob_greater_than_x1 = np.linspace(
                        stat.norm(mu, sigma).ppf(x1),
                        stat.norm(mu, sigma).ppf(0.9999),
                        10000)
                    norm_pdf = stat.norm(mu, sigma).pdf(prob_greater_than_x1)
                    fig.add_trace(
                        go.Scatter(x=prob_greater_than_x1,
                                   y=norm_pdf,
                                   name="Probability",
                                   marker_color=stat_colours["norm"],
                                   fill="tozeroy",
                                   fillcolor=stat_colours["z"]))
                    norm_pdf1 = norm_x
                    empirical_rule(fig, mu, sigma, norm_x)
        elif calc_type == "<>" or calc_type == "><":
            if z1 is None or z2 is None:
                return fig, True, True, "Enter values for z1 and z2", no_update, "", "", "", ""
            if z1 > z2:
                return fig, True, True, "z1 must be less than z2", no_update, "", "", "", ""
            else:
                sr_norm = f"Normal distribution with mean {mu}, standard deviation {sigma}, z1 = {z1} and z2 = {z2}"
                if calc_type == "<>":
                    max_z = max(z1, z2)
                    min_z = min(z1, z2)
                    x1 = stat.norm(mu, sigma).cdf(max_z)
                    x2 = stat.norm(mu, sigma).cdf(min_z)
                    probability = round((x1 - x2)*100, 2)
                    prob_between_x1_x2 = np.linspace(
                        stat.norm(mu, sigma).ppf(x1),
                        stat.norm(mu, sigma).ppf(x2),
                        10000)
                    norm_pdf = stat.norm(mu, sigma).pdf(prob_between_x1_x2)
                    fig.add_trace(
                        go.Scatter(x=prob_between_x1_x2,
                                    y=norm_pdf,
                                    name="Probability",
                                    marker_color=stat_colours["norm"],
                                    fill="tozeroy",
                                    fillcolor=stat_colours["z"]))
                    norm_pdf1 = norm_x
                    empirical_rule(fig, mu, sigma, norm_x)
                elif calc_type == "><":
                    x1 = stat.norm(mu, sigma).cdf(z1)
                    x2 = stat.norm(mu, sigma).cdf(z2)
                    probability = round((x1 + (1 - x2))*100, 2)
                    prob_less_than_x1 = np.linspace(
                        stat.norm(mu, sigma).ppf(0.0001),
                        stat.norm(mu, sigma).ppf(x1),
                        10000)
                    norm_pdf1 = stat.norm(mu, sigma).pdf(prob_less_than_x1)
                    prob_greater_than_x2 = np.linspace(
                        stat.norm(mu, sigma).ppf(x2),
                        stat.norm(mu, sigma).ppf(0.9999),
                        10000)
                    norm_pdf2 = stat.norm(mu, sigma).pdf(prob_greater_than_x2)
                    fig.add_trace(
                        go.Scatter(x=prob_less_than_x1,
                                    y=norm_pdf1,
                                    name="Probability",
                                    marker_color=stat_colours["norm"],
                                    fill="tozeroy",
                                    fillcolor=stat_colours["z"]))
                    fig.add_trace(
                        go.Scatter(x=prob_greater_than_x2,
                                    y=norm_pdf2,
                                    marker_color=stat_colours["norm"],
                                    fill="tozeroy",
                                    fillcolor=stat_colours["z"],
                                    showlegend=False))
                    empirical_rule(fig, mu, sigma, norm_x)
    return fig, False, False, "", {"display": "inline"}, f"{mu}", f"{sigma}", f"{probability}%", sr_norm


def empirical_rule(fig, mu, sigma, norm_pdf):
    fig.add_trace(
        go.Scatter(x=[mu] * 10,
                   y=np.linspace(0, max(norm_pdf), 10),
                   name="Mean",
                   marker_color=stat_colours["mean"],
                   marker_opacity=0,
                   hovertemplate="Mean: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(sigma + mu), 10),
                   name=u"Mean \u00B1 1SD",
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 1SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(sigma + mu), 10),
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 1SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(2*sigma + mu), 10),
                   name=u"Mean \u00B1 2SD",
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 2SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(2*sigma + mu), 10),
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 2SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(3*sigma + mu), 10),
                   name=u"Mean \u00B1 3SD",
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 3SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(3*sigma + mu), 10),
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 3SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.update_layout(dragmode=False)


@app.callback(
    Output("z1", "min"),
    Output("z1", "max"),
    Output("z2", "min"),
    Output("z2", "max"),
    Input("mu", "value"),
    Input("sigma", "value"),
    suppress_callback_exceptions=True
)
def set_z_min_max(mu, sigma):
    if mu is None or sigma is None:
        raise exceptions.PreventUpdate
    else:
        z1_min = -4*sigma + mu
        z1_max = 4*sigma + mu
        z2_min = -4*sigma + mu
        z2_max = 4*sigma + mu
    return z1_min, z1_max, z2_min, z2_max


@app.callback(
    Output("z1", "disabled"),
    Output("z2", "disabled"),
    Output("z1", "required"),
    Output("z2", "required"),
    Input("calc-type", "value"),
    prevent_initial_call=True
)
def display_z_inputs(calc_type):
    if calc_type is None:
        raise exceptions.PreventUpdate
    if calc_type == "<>" or calc_type == "><":
        return False, False, True, True
    else:
        return False, True, True, False


if __name__ == "__main__":
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    app.run(debug=True)