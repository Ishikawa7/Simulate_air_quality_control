# IMPORT LIBRARIES #####################################################################################################
import dash
from dash import dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/guide',
    )

layout = dbc.Container(
    [
        # markdown
        dcc.Markdown('''
        # Guida
        
        
        '''),
    ],
)

# Pagina della guida in markdown