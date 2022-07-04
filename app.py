from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

happy_df = pd.read_csv("data/happy.csv")

app = Dash(__name__,
           title="Total happiness",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(happy_df.columns[1:],
                         value="Sex",
                         id="cols-dropdown",
                         clearable=False)
        ], xs=12, sm=6, md=6, lg=6, xl=6),
        dbc.Col([
            html.P(
                "Select a categorical variable from the dropdown list to compare total happiness for different groups.",
                style={"font-weight": "bold"})
        ], xs=12, sm=6, md=6, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Descriptive statistics",
                   style={"text-align": "center",
                          "font-weight": "bold",
                          "margin": 0}),
            html.P(id="header1",
                   style={"text-align": "center",
                          "font-weight": "bold"}),
            html.Table([
                html.Tr([html.Td(["Mean:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="mean1", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Standard deviation:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="std1", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["First quartile:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="q1_1", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Median:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="median1", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Third quartile:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="q3_1", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Interquartile range:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="iqr1", style={"padding": "0 5px"})]),
            ], style={"margin": "0 auto"})
        ], xs=6, sm=6, md=6, lg=6, xl=6),
        dbc.Col([
            html.P("Descriptive statistics", style={
                   "text-align": "center", "font-weight": "bold", "margin": 0}),
            html.P(id="header2", style={
                "text-align": "center", "font-weight": "bold"}),
            html.Table([
                html.Tr([html.Td(["Mean:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="mean2", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Standard deviation:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="std2", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["First quartile:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="q1_2", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Median:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="median2", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Third quartile:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="q3_2", style={"padding": "0 5px"})]),
                html.Tr([html.Td(["Interquartile range:"], style={"text-align": "right", "padding": "0 5px"}),
                        html.Td(id="iqr2", style={"padding": "0 5px"})]),
            ], style={"margin": "0 auto"})
        ], xs=6, sm=6, md=6, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="output-hist1")
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dcc.Graph(id="output-hist2")
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="output-box1")
        ], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([
            dcc.Graph(id="output-box2")
        ], xs=12, sm=12, md=12, lg=6, xl=6)
    ])
])


@app.callback(
    Output("header1", "children"),
    Output("header2", "children"),
    Output("mean1", "children"),
    Output("std1", "children"),
    Output("q1_1", "children"),
    Output("median1", "children"),
    Output("q3_1", "children"),
    Output("iqr1", "children"),
    Output("mean2", "children"),
    Output("std2", "children"),
    Output("q1_2", "children"),
    Output("median2", "children"),
    Output("q3_2", "children"),
    Output("iqr2", "children"),
    Input("cols-dropdown", "value")
)
def update_statistics(value):
    stats_df = happy_df[["Total happiness", value]].dropna()
    categories = stats_df[value].unique()
    stats_df1 = stats_df["Total happiness"][(stats_df[value] == categories[0])]
    stats_df2 = stats_df["Total happiness"][(stats_df[value] == categories[1])]

    header1 = f"{value} = {categories[0]}"
    header2 = f"{value} = {categories[1]}"

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

    return header1, header2, mean1, std1, q1_1, median1, q3_1, iqr1, mean2, std2, q1_2, median2, q3_2, iqr2


@app.callback(
    Output("output-hist1", "figure"),
    Output("output-hist2", "figure"),
    Input("cols-dropdown", "value")
)
def update_histogram(value):
    hist_df = happy_df[["Total happiness", value]].dropna()
    categories = hist_df[value].unique()
    hist_df1 = hist_df["Total happiness"][(hist_df[value] == categories[0])]
    hist_df2 = hist_df["Total happiness"][(hist_df[value] == categories[1])]

    fig1 = px.histogram(hist_df1,
                        x="Total happiness",
                        histnorm="probability density",
                        range_x=[0, 28.5],
                        range_y=[0, 0.13])
    fig1.update_traces(marker_line_width=1,
                       marker_line_color="rgba(209,3,115,1)",
                       marker_color="rgba(209,3,115,0.5)")
    fig1.update_layout(margin=dict(t=10, b=10)),
    fig1.update_xaxes(title_text=f"Histogram of Total happiness for {value} = {categories[0]}",
                      dtick=7,
                      tick0=7)
    fig1.update_yaxes(title_text=None)
    fig1.add_vline(x=hist_df1.mean(),
                   line_color="#003896")
    fig1.add_vline(x=hist_df1.median(),
                   line_color="#006338")
    fig1.add_vline(x=hist_df1.mean() + hist_df1.std(),
                   line_color="#0085a1")
    fig1.add_vline(x=hist_df1.mean() - hist_df1.std(),
                   line_color="#0085a1")
    fig1.add_vline(x=hist_df1.quantile(0.25),
                   line_color="#6a2150")
    fig1.add_vline(x=hist_df1.quantile(0.75),
                   line_color="#6a2150")

    fig2 = px.histogram(hist_df2,
                        x="Total happiness",
                        histnorm="probability density",
                        range_x=[0, 28.5],
                        range_y=[0, 0.13])
    fig2.update_traces(marker_line_width=1,
                       marker_line_color="rgba(158,171,5,1)",
                       marker_color="rgba(158,171,5,0.5)")
    fig2.update_layout(margin=dict(t=10, b=10))
    fig2.update_xaxes(title_text=f"Histogram of Total happiness for {value} = {categories[1]}",
                      dtick=7,
                      tick0=7)
    fig2.update_yaxes(title_text="Frequency")
    fig2.add_vline(x=hist_df2.mean(),
                   line_color="#003896")
    fig2.add_vline(x=hist_df2.median(),
                   line_color="#006338")
    fig2.add_vline(x=hist_df2.mean() + hist_df2.std(),
                   line_color="#0085a1")
    fig2.add_vline(x=hist_df2.mean() - hist_df2.std(),
                   line_color="#0085a1")
    fig2.add_vline(x=hist_df2.quantile(0.25),
                   line_color="#6a2150")
    fig2.add_vline(x=hist_df2.quantile(0.75),
                   line_color="#6a2150")

    return fig1, fig2


@app.callback(
    Output("output-box1", "figure"),
    Output("output-box2", "figure"),
    Input("cols-dropdown", "value")
)
def update_boxplot(value):
    box_df = happy_df[["Total happiness", value]].dropna()
    categories = box_df[value].unique()
    box_df1 = box_df["Total happiness"][(box_df[value] == categories[0])]
    box_df2 = box_df["Total happiness"][(box_df[value] == categories[1])]

    fig1 = px.box(box_df1,
                  range_x=[0, 28.5],
                  orientation="h")
    fig1.update_traces(marker_color="#d10373")
    fig1.update_layout(margin=dict(t=10, b=10))
    fig1.update_xaxes(title_text=f"Boxplot of Total happiness for {value} = {categories[0]}",
                      dtick=7,
                      tick0=7)
    fig1.update_yaxes(visible=False,
                      showticklabels=False)
    fig1.add_vline(x=box_df1.mean(),
                   line_color="#003896")
    fig1.add_vline(x=box_df1.median(),
                   line_color="#006338")
    fig1.add_vline(x=box_df1.mean() + box_df1.std(),
                   line_color="#0085a1")
    fig1.add_vline(x=box_df1.mean() - box_df1.std(),
                   line_color="#0085a1")
    fig1.add_vline(x=box_df1.quantile(0.25),
                   line_color="#6a2150")
    fig1.add_vline(x=box_df1.quantile(0.75),
                   line_color="#6a2150")

    fig2 = px.box(box_df2,
                  range_x=[0, 28.5],
                  orientation="h")
    fig2.update_traces(marker_color="#9eab05")
    fig2.update_layout(margin=dict(t=10, b=10))
    fig2.update_xaxes(title_text=f"Boxplot of Total happiness for {value} = {categories[1]}",
                      dtick=7,
                      tick0=7)
    fig2.update_yaxes(visible=False,
                      showticklabels=False)
    fig2.add_vline(x=box_df1.mean(),
                   line_color="#003896")
    fig2.add_vline(x=box_df2.median(),
                   line_color="#006338")
    fig2.add_vline(x=box_df2.mean() + box_df2.std(),
                   line_color="#0085a1")
    fig2.add_vline(x=box_df2.mean() - box_df2.std(),
                   line_color="#0085a1")
    fig2.add_vline(x=box_df2.quantile(0.25),
                   line_color="#6a2150")
    fig2.add_vline(x=box_df2.quantile(0.75),
                   line_color="#6a2150")

    return fig1, fig2


if __name__ == "__main__":
    app.run_server(debug=True)
