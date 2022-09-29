from dash import Input, Output, State, exceptions, no_update
import math
import numpy as np
import plotly.graph_objects as go
import scipy.stats as stat
from nor_model import normal_distribution, calculate_probability_z1, calculate_probability_z1_z2, stat_colours
from nor_view import app

# app.callback Outputs and Inputs are all associated with unique elements in *_view.py though the first argument (component_id) and control/are controlled by the second argument (component_property)


# Callback function to update normal distribution graph, results and associated screen reader text based on user entry values (mu (mean), sigma (standard deviation), z1, z2 and calculation type)
@app.callback(
    # Graph
    Output("normal-dist-fig", "figure"),
    Output("sr-norm", "children"),
    # Input validation for z1 and z2
    Output("z1", "invalid"),
    Output("z2", "invalid"),
    Output("error", "children"),
    # Results hidden until callback triggered
    Output("results", "style"),
    # Results
    Output("current-mu", "children"),
    Output("current-sigma", "children"),
    Output("probability", "children"),
    # Inputs
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
        # Create base normal distribution graph from mean (mu) and standard deviation (sigma) user entry 
        x, norm_x = normal_distribution(mu, sigma)
        fig = go.Figure(
            go.Scatter(x=x,
                       y=norm_x,
                       dx=1,
                       x0=-4,
                       marker_color=stat_colours["norm"],
                       name="Normal distribution",
                       hoverinfo="skip"),
            layout={"margin": dict(t=20, b=10, l=20, r=20),
                    "height": 400,
                    "font_size": 14})
        fig.update_xaxes(dtick=math.ceil(sigma/2))
        # Add graph trace for Z < z1 or Z > z1
        if calc_type == "<" or calc_type == ">":
            # Input validation for z1
            if z1 is None:
                return fig, "", True, False, "Enter a value for z1", no_update, "", "", ""
            else:
                if calc_type == "<":
                    probability, prob_less_than_x1, norm_pdf = calculate_probability_z1(mu, sigma, z1, calc_type)
                    fig.add_trace(
                        go.Scatter(x=prob_less_than_x1,
                                   y=norm_pdf,
                                   name="Probability",
                                   marker_color=stat_colours["norm"],
                                   fill="tozeroy",
                                   fillcolor=stat_colours["z"],
                                   hoveron="fills"))
                    empirical_rule(fig, mu, sigma, norm_x)
                    # Screen reader text
                    sr_norm = f"Normal distribution graph with mean {mu}, standard deviation {sigma} and probability that Z is less than {z1} of {probability}%"
                elif calc_type == ">":
                    probability, prob_greater_than_x1, norm_pdf = calculate_probability_z1(mu, sigma, z1, calc_type)
                    fig.add_trace(
                        go.Scatter(x=prob_greater_than_x1,
                                   y=norm_pdf,
                                   name="Probability",
                                   marker_color=stat_colours["norm"],
                                   fill="tozeroy",
                                   fillcolor=stat_colours["z"]))
                    empirical_rule(fig, mu, sigma, norm_x)
                                        # Screen reader text
                    sr_norm = f"Normal distribution graph with mean {mu}, standard deviation {sigma} and probability that Z is greater than {z1} of {probability}%"
        # Add graph trace(s) for z1 < Z < z2 or Z < z1 and Z > z2
        elif calc_type == "<>" or calc_type == "><":
            # Input validation for z1 and z2
            if z1 is None or z2 is None:
                return fig, "", True, True, "Enter values for z1 and z2", no_update, "", "", ""
            if z1 > z2:
                return fig, "", True, True, "z1 must be less than z2", no_update, "", "", ""
            else:
                if calc_type == "<>":
                    probability, prob_between_x1_x2, norm_pdf = calculate_probability_z1_z2(mu, sigma, z1, z2, calc_type)
                    fig.add_trace(
                        go.Scatter(x=prob_between_x1_x2,
                                   y=norm_pdf,
                                   name="Probability",
                                   marker_color=stat_colours["norm"],
                                   fill="tozeroy",
                                   fillcolor=stat_colours["z"]))
                    empirical_rule(fig, mu, sigma, norm_x)
                    # Screen reader text
                    sr_norm = f"Normal distribution with mean {mu}, standard deviation {sigma}, and probability that Z is between {z1} and {z2} of {probability}%"
                elif calc_type == "><":
                    probability, prob_less_than_x1, prob_greater_than_x2, norm_pdf1, norm_pdf2 = calculate_probability_z1_z2(mu, sigma, z1, z2, calc_type)
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
                    # Screen reader text
                    sr_norm = f"Normal distribution with mean {mu}, standard deviation {sigma}, and probability that Z is less than {z1} and greater than {z2} of {probability}%"
    return fig, sr_norm, False, False, "", {"display": "inline"}, f"{mu}", f"{sigma}", f"{probability}%"


# Add graph lines for mean and +/-1/2/3SD for mean (mu) and standard deviation (sigma) user entry
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
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(sigma + mu), 10),
                   name=u"Mean \u00B1 1SD",
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 1SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(sigma + mu), 10),
                   marker_color=stat_colours["+-1std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 1SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(2*sigma + mu), 10),
                   name=u"Mean \u00B1 2SD",
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 2SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-2*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(2*sigma + mu), 10),
                   marker_color=stat_colours["+-2std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 2SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.add_trace(
        go.Scatter(x=[3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(3*sigma + mu), 10),
                   name=u"Mean \u00B1 3SD",
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean + 3SD: %{x:.3f}<extra></extra>"))
    fig.add_trace(
        go.Scatter(x=[-3*sigma + mu] * 10,
                   y=np.linspace(0, stat.norm(mu, sigma).pdf(3*sigma + mu), 10),
                   marker_color=stat_colours["+-3std"],
                   marker_opacity=0,
                   hovertemplate="Mean - 3SD: %{x:.3f}<extra></extra>",
                   showlegend=False))
    fig.update_layout(dragmode=False)


# Set minimum and maximum values for z1 and z2 for mean (mu) and standard deviation (sigma) user entry - values entered outside this range do not generate meaningful results
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


# Enable/disable z1 and z2 input fields based on selected calculation type
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
    # app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
