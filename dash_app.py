import dash
import flask

import dash_bootstrap_components as dbc

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, 
                server=server,
                external_stylesheets=[dbc.themes.UNITED])

app.config.suppress_callback_exceptions = True
