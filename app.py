import dash
from dash import Dash, Input, Output, State, callback, html, dcc
import dash_bootstrap_components as dbc

# css file for dash components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# DASH APP #############################################################################################################
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SANDSTONE, dbc_css]) #suppress_callback_exceptions=True

def create_app_layout():
    return dbc.Container(
        [
            dbc.NavbarSimple(
                id = "navbar",
                children=[
                    dbc.NavItem(dbc.NavLink("Pagina iniziale", href="/", style={'font-size': '15px'})),
                    dbc.NavItem(dbc.NavLink("Guida", href="/guide", style={'font-size': '15px'})),
                    #html.Img(src='/static/icons/Logo_COR.png', height="100px"),
                    ## add space between images
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons/Logo_semeion.png', height="100px"),
                    #html.Div(style={'display': 'inline-block', 'width': '5px'}),
                    #html.Img(src='/static/icons/Logo_semeiontech.png', height="100px"),
                ],
                brand="PROTOTIPO AIR CONTROLLER",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            html.Hr(),
            # temp for showing all pages
            html.Div(
                [
                    dbc.Button(
                        "Pagine",
                        id="collapse-button-nav",
                        className="mb-3",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        html.Div([
                            html.Div(
                                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
                            ) for page in dash.page_registry.values()
                        ]),
                        id="collapse-nav",
                    ),
                ]
            ),
            #########################
    	    dash.page_container,
            # add a footer
            html.Hr(),
            # use a jumbotron to add a description for the app
            html.Div(
                dbc.Container(
                    [
                        html.H3("Informazioni utili"),
                        html.P(
                            "Simulazione",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            "Per avere informazioni consultare la guida."
                        ),
                        html.P(
                            dbc.Button("Guida", color="primary", href='/guide'), className="lead"
                        ),
                    ],
                    fluid=True,
                    className="py-3",
                ),
                className="p-3 bg-light rounded-3",
            )
        ],
        fluid=True,
    )

app.layout = create_app_layout

#CALLBACKS #######################################################################################################

@app.callback(
    Output("collapse-nav", "is_open"),
    [Input("collapse-button-nav", "n_clicks")],
    [State("collapse-nav", "is_open")],
    prevent_initial_call=True
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# RUN THE APP ###########################################################################################################
if __name__ == "__main__":
    # shut down any running dash processes
    #os.system("taskkill /f /im python.exe")
    # start the dash app
    #app.run_server(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    app.run_server(debug=True, use_reloader=True)

# if Python [Errno 98] Address already in use 
# kill -9 $(ps -A | grep python | awk '{print $1}')
    
# In questo script, viene definita un'applicazione Dash per la visualizzazione di analisi e risultati
# relativi a un progetto chiamato "PROGETTO P_RAM". L'app utilizza il framework Dash di Plotly
# e il tema "SANDSTONE" di dash-bootstrap-components per la presentazione grafica.

# ESTERNAZIONE DELLE RISORSE CSS:
# Viene dichiarato un link esterno a un file CSS di stile, utilizzato per personalizzare l'aspetto
# degli elementi Dash. Il file viene caricato da un repository CDN.

# LAYOUT DELL'APP:
# Viene definita la funzione create_app_layout(), che genera il layout principale dell'app.
# Questo layout include una barra di navigazione con link a pagine specifiche, un bottone per mostrare/nascondere
# l'elenco delle pagine disponibili, un contenitore per visualizzare le pagine, e una sezione con informazioni
# aggiuntive e link alla guida del progetto.

# CALLBACKS:
# Viene definita una callback per gestire l'apertura/chiusura dell'elenco delle pagine quando si fa clic sul bottone.

# RUN THE APP:
# L'app viene inizializzata e avviata utilizzando Dash. L'app è accessibile all'indirizzo http://0.0.0.0:8080/,
# e il debug è disabilitato per l'utilizzo in produzione.