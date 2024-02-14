# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc
from simulator import Simulator

dash.register_page(
    __name__,
    path='/',
    )

# LOAD RESOURCES #######################################################################################################
simulator = Simulator()

def create_layout_home():

    return dbc.Container(
        [
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("People(n)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-people_minus", n_clicks=0),
                                    dbc.Input(id="value-people", placeholder="0", disabled=True, value=0),
                                    dbc.Button("+", id="input-people_plus", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("Volume(m^3)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-volume_minus", n_clicks=0),
                                    dbc.Input(id="value-volume", placeholder="27", disabled=True, value=27), # 10 m^2
                                    dbc.Button("+", id="input-volume_plus", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("Pump capacity(L/min)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpL_minus", n_clicks=0),
                                    dbc.Input(id="value-pumpL", placeholder="566", disabled=True, value=566),#566 = 10 cfm
                                    dbc.Button("+", id="input-pumpL_plus", n_clicks=0),
                                ]
                            ),
                        ]
                    ),
                    dbc.Col(
                        [
                            html.H5("N pumps"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-pumpN_minus", n_clicks=0),
                                    dbc.Input(id="value-pumpN", placeholder="4", disabled=True, value=4),
                                    dbc.Button("+", id="input-pumpN_plus", n_clicks=0),
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
                        [dcc.Graph(id="CO-graph")],
                        width=9,
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            html.Br(),
                            html.H6("Pump power(%)"),
                            dbc.Progress(label="0%", value=0, id="pump-power"),
                            html.Br(),
                            html.Br(),
                            html.H6("People average last 10 minutes"),
                            dbc.Badge("0", className="ms-1"),
                            html.Br(),
                            html.Br(),
                            html.H6("CO threshold(mg/m^3)"),
                            dbc.InputGroup(
                                [
                                    dbc.Button("-", id="input-threshold_minus", n_clicks=0),
                                    dbc.Input(id="value-threshold", placeholder="0", disabled=True, value=5.725),
                                    dbc.Button("+", id="input-threshold_plus", n_clicks=0),
                                ]
                            ),
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
            dcc.Interval(
                id='interval-component',
                interval=1*10000, # in milliseconds
                n_intervals=0
            )
        ],
    )
layout = create_layout_home

@callback(
    [
        Output("pump-power", "value"),
        Output("pump-power", "label"),
        Output("CO-graph", "figure"),
    ],
    [
        Input('interval-component', 'n_intervals')
    ]
)
def simulation(n_intervals):
    if n_intervals != 0:
        if not simulator.active:
            return 0, "0%", px.line(template="plotly_white")
        else:
            simulator.simulate_time_step()
            pump_power = simulator.pump_power
            df_sim = simulator.df_sim
            predictions = simulator.predictions
            print(predictions)
            print(df_sim)
            fig = go.Figure()
            # Create and style traces
            fig.add_trace(go.Scatter(x=df_sim.index, y=df_sim["CO(mg/m^3)_final"].values, name='CO(mg/m^3)',
                                     line=dict(color='green', width=4)))
            fig.add_trace(go.Scatter(x=[i for i in range(df_sim.index[-1],df_sim.index[-1]+11)], y=predictions, name='CO(mg/m^3) predicted',
                                     line=dict(color='blue', width=4,
                                          dash='dash')
            ))
            fig.add_trace(go.Scatter(x=[i for i in range(0,df_sim.index[-1]+10)], y=[simulator.threshold for i in range(0,df_sim.index[-1]+10)], name='Threshold(mg/m^3)',
                                     line=dict(color='firebrick', width=4,
                                          dash='dot')
            ))
            #fig = px.line(df_sim, x=df_sim.index, y="CO(mg/m^3)_final", title="CO(mg/m^3)", markers=True, template="plotly_white")
            fig.update_xaxes(title_text="Time(min)")
            fig.update_yaxes(title_text="CO(mg/m^3)")
            fig.update_layout(transition_duration=500)
            # change theme
            fig.update_layout(template="plotly_white")
            return pump_power, str(pump_power)+'%', fig
    else:
        return 0, '0%',px.line(template="plotly_white")

# create a callback for the input-people_minus button and the input-people_plus button that will update the value-people input
@callback(
    Output("value-people", "value"),
    [
        Input("input-people_minus", "n_clicks"),
        Input("input-people_plus", "n_clicks"),
    ],
    [
        State("value-people", "value"),
    ]
)
def update_people(n_minus, n_plus, value):
    # Extracting the button that triggered the callback
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_button == "input-people_minus" and int(value) > 0:
        value = int(value) - 1
    elif triggered_button == "input-people_plus" and int(value) < 10:
        value = int(value) + 1
    
    simulator.people_now = value
    return value

# create a callback for the input-volume_minus button and the input-volume_plus button that will update the value-volume input
@callback(
    Output("value-volume", "value"),
    [
        Input("input-volume_minus", "n_clicks"),
        Input("input-volume_plus", "n_clicks"),
    ],
    [
        State("value-volume", "value"),
    ]
)
def update_volume(n_minus, n_plus, value):
    # Extracting the button that triggered the callback
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_button == "input-volume_minus" and int(value) > 10:
        value = int(value) - 1
    elif triggered_button == "input-volume_plus" and int(value) < 30:
        value = int(value) + 1
    
    simulator.volume = value
    return value

# create a callback for the input-pumpL_minus button and the input-pumpL_plus button that will update the value-pumpL input
@callback(
    Output("value-pumpL", "value"),
    [
        Input("input-pumpL_minus", "n_clicks"),
        Input("input-pumpL_plus", "n_clicks"),
    ],
    [
        State("value-pumpL", "value"),
    ]
)
def update_pumpL(n_minus, n_plus, value):
    # Extracting the button that triggered the callback
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_button == "input-pumpL_minus" and int(value) > 141:
        value = int(value) - 1
    elif triggered_button == "input-pumpL_plus" and int(value) < 708:
        value = int(value) + 1
    
    simulator.pumps_l_min = value
    return value

# create a callback for the input-pumpN_minus button and the input-pumpN_plus button that will update the value-pumpN input
@callback(
    Output("value-pumpN", "value"),
    [
        Input("input-pumpN_minus", "n_clicks"),
        Input("input-pumpN_plus", "n_clicks"),
    ],
    [
        State("value-pumpN", "value"),
    ]
)
def update_pumpN(n_minus, n_plus, value):
    # Extracting the button that triggered the callback
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_button == "input-pumpN_minus" and int(value) > 1:
        value = int(value) - 1
    elif triggered_button == "input-pumpN_plus" and int(value) < 8:
        value = int(value) + 1
    
    simulator.n_pumps = value
    return value

# create a callback for the input-threshold_minus button and the input-threshold_plus button that will update the value-threshold input
@callback(
    Output("value-threshold", "value"),
    [
        Input("input-threshold_minus", "n_clicks"),
        Input("input-threshold_plus", "n_clicks"),
    ],
    [
        State("value-threshold", "value"),
    ]
)
def update_threshold(n_minus, n_plus, value):
    # Extracting the button that triggered the callback
    triggered_button = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if triggered_button == "input-threshold_minus" and int(value) > 0:
        value = int(value) - 1
    elif triggered_button == "input-threshold_plus" and int(value) < 10:
        value = int(value) + 1
    
    simulator.threshold = value
    return value