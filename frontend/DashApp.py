from dash import Dash, dcc, html, Input, Output, State, callback, dash_table, dash
from dash.dependencies import Input, Output
from dash import callback_context
import dash_bootstrap_components as dbc
import dash

# from frontend.pages import programSearch

import json


def Generate_Dash_App():

    app = Dash(__name__, use_pages=True)

    app.layout = html.Div(children=[

    html.Div(
        children=[
            html.H1(
                children='Education Analysis Dashboard', className='main-header'
            ),
            html.Div([
            dcc.Link(page['name']+"  |  ", href=page['path'], className='mainnav-link')
            for page in dash.page_registry.values()
            ]),
            html.Hr(),
            dash.page_container
            
        ]
    ),

    

    


    ], style={'font-family':'Arial', 'font-size': '20px'})

    # programSearch.register_callbacks(app=app)
    

    return app