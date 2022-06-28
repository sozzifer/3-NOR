from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

happy_df = pd.read_csv("happy.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([dcc.Dropdown(happy_df.columns[1:], value="Sex",
                 id="cols-dropdown", clearable=False)])
    ], id="dropdown"),
    html.Div([
        html.P("Select a categorical variable from the dropdown list to compare total happiness for different groups.")
    ]),
    html.Div([
        html.Div(id="output-stats1", style={
            'width': '40%', 'display': 'inline-block', "padding": "20px"}),
        html.Div(id="output-stats2", style={
            'width': '40%', 'float': 'right', 'display': 'inline-block', "padding": "20px"})
    ], style={"width": "90%"}),
    html.Div([
        html.Div([dcc.Graph(id="output-hist1")],
                 style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id="output-hist2")],
                 style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], id="histograms"),
    html.Div([
        html.Div([dcc.Graph(id="output-box1")],
                 style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id="output-box2")],
                 style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], id="boxplots")
])


@app.callback(
    Output("output-stats1", "children"),
    Output("output-stats2", "children"),
    Input("cols-dropdown", "value")
)
def update_statistics(value):
    stats_df = happy_df[["Total happiness", value]].dropna()
    categories = stats_df[value].unique()
    stats_df1 = stats_df["Total happiness"][(stats_df[value] == categories[0])]
    stats_df2 = stats_df["Total happiness"][(stats_df[value] == categories[1])]
    mean1 = round(stats_df1.mean(), 3)
    mean2 = round(stats_df2.mean(), 3)
    std1 = round(stats_df1.std(), 3)
    std2 = round(stats_df2.std(), 3)
    q1_1 = stats_df1.quantile(0.25)
    q1_2 = stats_df2.quantile(0.25)
    median1 = stats_df1.median()
    median2 = stats_df2.median()
    q3_1 = stats_df1.quantile(0.75)
    q3_2 = stats_df2.quantile(0.75)
    iqr1 = q3_1 - q1_1
    iqr2 = q3_2 - q1_2

    return [html.H3(f"Descriptive statistics for {value} = {categories[0]}"), html.P(f"Mean: {mean1}"), html.P(f"Standard deviation: {std1}"), html.P(f"First quartile: {q1_1}"), html.P(f"Median: {median1}"), html.P(f"Third quartile: {q3_1}"), html.P(f"Interquartile range: {iqr1}")], [html.H3(f"Descriptive statistics for {value} = {categories[1]}"), html.P(f"Mean: {mean2}"), html.P(f"Standard deviation: {std2}"), html.P(f"First quartile: {q1_2}"), html.P(f"Median: {median2}"), html.P(f"Third quartile: {q3_2}"), html.P(f"Interquartile range: {iqr2}")]


@app.callback(
    Output("output-hist1", "figure"),
    Output("output-hist2", "figure"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    hist_df = happy_df[["Total happiness", value]].dropna()
    categories = hist_df[value].unique()
    hist_df1 = hist_df[(hist_df[value] == categories[0])]
    hist_df2 = hist_df[(hist_df[value] == categories[1])]
    fig1 = px.histogram(hist_df1,
                        x="Total happiness",
                        histnorm="probability density",
                        title=categories[0],
                        range_x=[0, 28.5],
                        range_y=[0, 0.13])
    fig1.update_traces(marker_line_width=1, marker_line_color="white")
    fig1.update_layout(title_x=0.5)
    fig1.update_xaxes(
        title_text=f"Total happiness for {value} = {categories[0]}", dtick=7, tick0=7)
    fig1.update_yaxes(title_text="Frequency")
    fig2 = px.histogram(hist_df2,
                        x="Total happiness",
                        histnorm="probability density",
                        title=categories[1],
                        range_x=[0, 28.5],
                        range_y=[0, 0.13])
    fig2.update_traces(marker_line_width=1,
                       marker_line_color="white", marker_color="red")
    fig2.update_layout(title_x=0.5)
    fig2.update_xaxes(
        title_text=f"Total happiness for {value} = {categories[1]}", dtick=7, tick0=7)
    fig2.update_yaxes(title_text="Frequency")
    return fig1, fig2


@app.callback(
    Output("output-box1", "figure"),
    Output("output-box2", "figure"),
    Input("cols-dropdown", "value")
)
def update_boxplot(value):
    box_df = happy_df[["Total happiness", value]].dropna()
    categories = box_df[value].unique()
    box_df1 = box_df[(box_df[value] == categories[0])]
    box_df2 = box_df[(box_df[value] == categories[1])]

    fig1 = px.box(box_df1["Total happiness"],
                  range_x=[0, 28.5], orientation="h")
    fig1.update_traces(boxmean="sd")
    fig1.update_xaxes(
        title_text=f"Total happiness for {value} = {categories[0]}", dtick=7, tick0=7, showgrid=False)
    fig1.update_yaxes(visible=False, showticklabels=False)

    fig2 = px.box(box_df2["Total happiness"],
                  range_x=[0, 28.5], orientation="h")
    fig2.update_traces(boxmean="sd", marker_color="red")
    fig2.update_xaxes(
        title_text=f"Total happiness for {value} = {categories[1]}", dtick=7, tick0=7, showgrid=False)
    fig2.update_yaxes(visible=False, showticklabels=False)
    return fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
