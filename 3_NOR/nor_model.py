import numpy as np
import plotly.graph_objects as go
import scipy.stats as stat

# Colour palette
stat_colours = {
    "norm": "#d10373",
    "z": "rgba(158, 171, 5, 0.5)",
    "mean": "#f49103",
    "+-1std": "#0085a1",
    "+-2std": "#003896",
    "+-3std": "#006338"
}


# Generate normal distribution for mean (mu) and standard deviation (sigma) user entry
def normal_distribution(mu, sigma):
    x = np.linspace(stat.norm(mu, sigma).ppf(0.0001),
                    stat.norm(mu, sigma).ppf(0.9999),
                    10000)
    norm_x = stat.norm(mu, sigma).pdf(x)
    return x, norm_x


# Calculate probability for selected calculation type "Z < z1" or "Z > z1"
def calculate_probability_z1(mu, sigma, z1, calc_type):
    x1 = stat.norm(mu, sigma).cdf(z1)
    if calc_type == "<":
        probability = round(x1*100, 2)
        prob_less_than_x1 = np.linspace(stat.norm(mu, sigma).ppf(0.0001),
                                        stat.norm(mu, sigma).ppf(x1),
                                        10000)
        norm_pdf = stat.norm(mu, sigma).pdf(prob_less_than_x1)
        return probability, prob_less_than_x1, norm_pdf
    elif calc_type == ">":
        probability = round((1 - x1)*100, 2)
        prob_greater_than_x1 = np.linspace(stat.norm(mu, sigma).ppf(x1),
                                           stat.norm(mu, sigma).ppf(0.9999),
                                           10000)
        norm_pdf = stat.norm(mu, sigma).pdf(prob_greater_than_x1)
        return probability, prob_greater_than_x1, norm_pdf


# Calculate probability for selected calculation type "z1 < Z < z2" or "Z < z1 and Z > z2"
def calculate_probability_z1_z2(mu, sigma, z1, z2, calc_type):
    if calc_type == "<>":
        x1 = stat.norm(mu, sigma).cdf(max(z1, z2))
        x2 = stat.norm(mu, sigma).cdf(min(z1, z2))
        probability = round((x1 - x2)*100, 2)
        prob_between_x1_x2 = np.linspace(stat.norm(mu, sigma).ppf(x1),
                                         stat.norm(mu, sigma).ppf(x2),
                                         10000)
        norm_pdf = stat.norm(mu, sigma).pdf(prob_between_x1_x2)
        return probability, prob_between_x1_x2, norm_pdf
    elif calc_type == "><":
        x1 = stat.norm(mu, sigma).cdf(z1)
        x2 = stat.norm(mu, sigma).cdf(z2)
        probability = round((x1 + (1 - x2))*100, 2)
        prob_less_than_x1 = np.linspace(stat.norm(mu, sigma).ppf(0.0001),
                                        stat.norm(mu, sigma).ppf(x1),
                                        10000)
        norm_pdf1 = stat.norm(mu, sigma).pdf(prob_less_than_x1)
        prob_greater_than_x2 = np.linspace(stat.norm(mu, sigma).ppf(x2),
                                           stat.norm(mu, sigma).ppf(0.9999),
                                           10000)
        norm_pdf2 = stat.norm(mu, sigma).pdf(prob_greater_than_x2)
        return probability, prob_less_than_x1, prob_greater_than_x2, norm_pdf1, norm_pdf2


# Create blank figure with lines for mean, +-1/2/3SD; mean (mu) = 0, standard deviation (sigma) = 1
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
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(sigma + mu), 10),
                   name=u"Mean \u00B1 1SD",
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 1SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(sigma + mu), 10),
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 1SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    blank_fig.add_trace(
        go.Scatter(x=[2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(2*sigma + mu), 10),
                   name=u"Mean \u00B1 2SD",
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 2SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(2*sigma + mu), 10),
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 2SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    blank_fig.add_trace(
        go.Scatter(x=[3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(3*sigma + mu), 10),
                   name=u"Mean \u00B1 3SD",
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 3SD: %{x:.3f}<extra></extra>"))
    blank_fig.add_trace(
        go.Scatter(x=[-3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(3*sigma + mu), 10),
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 3SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    blank_fig.update_layout(dragmode=False)
    return blank_fig
