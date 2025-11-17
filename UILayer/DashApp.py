'''
This is the app module that serves as the entry point. It registers all pages and initializes the layout of the dash application
and the depedencies between the pages. 
'''



from dash import Dash, dcc, html, Input, Output, State, callback, dash_table, dash
from dash.dependencies import Input, Output
from dash import callback_context
import dash_bootstrap_components as dbc
import dash
import json

#Function for generating the Dash App.
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