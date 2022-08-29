import plotly.graph_objects as go
import scipy.stats as stat
import numpy as np

stat_colours = {
    "norm": "#d10373",
    "z": "rgba(158, 171, 5, 0.5)",
    "mean": "#f49103",
    "+-1std": "#0085a1",
    "+-2std": "#003896",
    "+-3std": "#006338"
}


def create_blank_fig():
    x = np.linspace(stat.norm.ppf(0.0001),
                    stat.norm.ppf(0.9999),
                    10000)
    norm_x = stat.norm.pdf(x)
    mu = 0
    sigma = 1
    blank_fig = go.Figure(
        go.Scatter(x=x,
                   y=norm_x,
                   name="Normal distribution",
                   marker_color=stat_colours["norm"],
                   hoverinfo="skip"),
        layout={"margin": dict(t=20, b=10, l=20, r=20),
                "height": 400,
                "font_size": 14})
    blank_fig.add_trace(
        go.Scatter(x=[mu] * 10,
                   y=np.linspace(0, max(norm_x), 10),
                   name="Mean",
                   marker_color=stat_colours["mean"],
                   marker_opacity=0,
                   hovertemplate="Mean: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(sigma + mu), 10),
                   name=u"Mean \u00B1 1SD",
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 1SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(sigma + mu), 10),
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 1SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    blank_fig.add_trace(
        go.Scatter(x=[2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(2*sigma + mu), 10),
                   name=u"Mean \u00B1 2SD",
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 2SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(2*sigma + mu), 10),
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 2SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    blank_fig.add_trace(
        go.Scatter(x=[3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(3*sigma + mu), 10),
                   name=u"Mean \u00B1 3SD",
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 3SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(
                       mu, sigma).pdf(3*sigma + mu), 10),
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 3SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    return blank_fig

