from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dis_model import happy_df

app = Dash(__name__,
           title="Total happiness",
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        html.H1("Summarising and illustrating data")
    ]),
    dbc.Row([
        html.P("The Happy dataset contains 1170 responses to a questionnaire about students' levels of happiness on a scale of 0 to 28, as well as the student's sex, if they are a UK student or not, and whether they consider themselves to be extroverted/introverted, absorbed and bored. Select a categorical variable from the dropdown list below to compare total happiness for different groups.")
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id="cols-dropdown",
                         options=[{"label": x, "value": x}
                                  for x in happy_df.columns[1:]],
                         value="Sex",
                         clearable=False)
        ], style={"margin":"auto"}, xs=12, sm=3, md=3, lg=3, xl=3)
    ], class_name="justify-content-center"),
    dbc.Row([
        dbc.Button("Descriptive statistics", id="toggle", n_clicks=0)
    ], class_name="justify-content-center"),
    dbc.Row([
            dbc.Col([
                dbc.Collapse([
                    dbc.Card([
                        dbc.CardBody([
                            html.Table(className="desc", children=[
                                html.Thead([
                                    html.Th(id="category1", className="right"),
                                    html.Th(id="group1"),
                                    html.Th(children=["Key"])
                                ]),
                                html.Tr([html.Td(className="right", children=["Sample size:"]),
                                         html.Td(id="n1")
                                ]), 
                                html.Tr([html.Td(className="right", children=["Mean:"]),
                                         html.Td(id="mean1"),
                                         html.Td(
                                            html.Span(className="mean-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Median:"]),
                                         html.Td(id="median1"),
                                         html.Td(
                                            html.Span(className="median-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Standard deviation (SD):"]),
                                         html.Td(
                                             id="std1", children=[]),
                                         html.Td(
                                            html.Span(className="std-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["First quartile:"]),
                                         html.Td(id="q1_1"),
                                         html.Td(
                                            html.Span(className="q1-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Third quartile:"]),
                                         html.Td(id="q3_1"),
                                         html.Td(
                                            html.Span(className="q3-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Interquartile range:"]),
                                         html.Td(id="iqr1")
                                ])
                            ])
                        ])
                    ], id="card1", style={"margin": "auto"})
                ], class_name="justify-content-center", id="collapse1", is_open=False)
            ], xs=8, sm=8, md=6, lg=6, xl=6, style={"margin": "auto"}),
            dbc.Col([
                dbc.Collapse([
                    dbc.Card([
                        dbc.CardBody([
                            html.Table(className="desc", children=[
                                html.Thead([
                                    html.Th(id="category2", className="right"),
                                    html.Th(id="group2"),
                                    html.Th(children=["Key"])
                                ]),
                                html.Tr([html.Td(className="right", children=["Sample size:"]),
                                         html.Td(id="n2")
                                ]),
                                html.Tr([html.Td(className="right", children=["Mean:"]),
                                         html.Td(id="mean2"),
                                         html.Td(
                                            html.Span(className="mean-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Median:"]),
                                         html.Td(id="median2"),
                                         html.Td(
                                            html.Span(className="median-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Standard deviation (SD):"]),
                                         html.Td(id="std2"),
                                         html.Td(
                                            html.Span(className="std-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["First quartile (Q1):"]),
                                         html.Td(id="q1_2"),
                                         html.Td(
                                            html.Span(className="q1-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Third quartile (Q3):"]),
                                         html.Td(id="q3_2"),
                                         html.Td(
                                            html.Span(className="q3-line"))
                                ]),
                                html.Tr([html.Td(className="right", children=["Interquartile range:"]),
                                         html.Td(id="iqr2")
                                ])
                            ])
                        ])
                    ], id="card2", style={"margin": "auto"})
                ], class_name="justify-content-center", id="collapse2", is_open=False)
            ], xs=8, sm=8, md=6, lg=6, xl=6, style={"margin": "auto"})
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

# , xs=6, sm=6, md=6, lg=6, xl=6
