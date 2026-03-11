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
    dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.FLATLY, dbc_css])

    navbar = dbc.NavbarSimple(
        brand="Education Analysis Dashboard",
        brand_href="/",
        color="primary",
        dark=True,
        className="navbar me-auto",
        children=[
            dbc.Button(dbc.NavLink(page["name"], href=page["path"]), className='mainnav-button btn')
            for page in dash.page_registry.values()
        ]
    )

    app.layout = dbc.Container(
        [   
            navbar,
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.Div(dash.page_container)
                        ]
                    )
                ],
                className="shadow-sm p-3 mb-5 bg-white rounded"
            )
        ],
        fluid=True,
        className="p-4",
    )

    

    return app