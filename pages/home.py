# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/',
    )

# LOAD RESOURCES #######################################################################################################

def create_layout_home():

    return dbc.Container(
        [
            dbc.Row(html.H1("Air Quality Simulator", className="text-center")),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("People(n)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-people", n_clicks=0),
                                    dbc.Input(id="value-people", placeholder="0"),
                                    dbc.Button("+", id="input-people", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("Volume(m^3)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-volume", n_clicks=0),
                                    dbc.Input(id="value-volume", placeholder="20"),
                                    dbc.Button("+", id="input-volume", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("Pump capacity(L/min)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpL", n_clicks=0),
                                    dbc.Input(id="value-pumpL", placeholder="0"),
                                    dbc.Button("+", id="input-pumpL", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("N pumps"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpN", n_clicks=0),
                                    dbc.Input(id="value-pumpN", placeholder="0"),
                                    dbc.Button("+", id="input-pumpN", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                ]
            ),
            # horizontal line
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph()],
                        width=9,
                    ),
                    dbc.Col(
                        [
                            html.H6("Pump power(%)"),
                            dbc.Progress(label="25%", value=25),
                            html.Br(),
                            html.Br(),
                            html.H6(["People average last 10 minutes", dbc.Badge("0", className="ms-1")]),
                            html.Br(),
                            html.Br(),
                            # add threshold ###################################################################################################
                        ],
                        width=3,
                    ),
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Button("Start simulation", color="primary", className="me-1"),
                            html.Div(style={'display': 'inline-block', 'width': '250px'}),
                            dbc.Button("Cancel simulation", color="danger", className="me-1"),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
    )
layout = create_layout_home
#@app.callback(
#    Output("example-output", "children"), [Input("example-button", "n_clicks")]
#)
#def on_button_click(n):
#    if n is None:
#        return "Not clicked."
#    else:
#        return f"Clicked {n} times."
