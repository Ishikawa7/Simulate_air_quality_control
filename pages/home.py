# IMPORT LIBRARIES #####################################################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, Input, Output, State, callback, html, dash_table, dcc
import dash_bootstrap_components as dbc
import json

import base64
import io
from data import DataClass

dash.register_page(
    __name__,
    path='/',
    )

# LOAD RESOURCES #######################################################################################################

def create_layout_home():

    return dbc.Container(
        [
            dbc.Button("Start simulation", color="primary", className="me-1"),
        ],
    )

#@app.callback(
#    Output("example-output", "children"), [Input("example-button", "n_clicks")]
#)
#def on_button_click(n):
#    if n is None:
#        return "Not clicked."
#    else:
#        return f"Clicked {n} times."
