from dash import dcc, html, callback ,Input, Output
import dash 
import dash_bootstrap_components as dbc

from UILayer.DashAppUtilities import (Get_Program_Options, Get_NOC_Options, Generate_Program_Pathways, Generate_NOC_History_In_Ontario, Generate_NOC_Latest_ER_PCT)

dash.register_page(
    __name__,
    path="/careerPathways",
    name="Career Pathways"
    )

layout = dbc.Container(
    [

        # ---------- PAGE TITLE ----------
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Program Career Pathways",
                    className="text-start mt-3 mb-4",
                    style={"font-size": "35px"}
                ),
                width=12
            )
        ),

        # ---------- PROGRAM DROPDOWN ----------
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label(
                        "Select Program",
                        className="fw-bold mb-2",
                        style={"font-size": "20px"}
                    ),
                    dcc.Dropdown(
                        id='Select_Program',
                        options=Get_Program_Options(),
                        multi=False,
                        className="mb-3"
                    ),
                    dcc.Graph(id='Graph_ProgramMap')
                ]
            ),
            className="shadow-sm mb-4"
        ),

        # ---------- NOC DROPDOWN ----------
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label(
                        "Select NOC Occupation",
                        className="fw-bold mb-2",
                        style={"font-size": "20px"}
                    ),
                    dcc.Dropdown(
                        id='Select_NOC',
                        options=Get_NOC_Options(),
                        multi=False,
                        className="mb-3"
                    )
                ]
            ),
            className="shadow-sm mb-4"
        ),

        # ---------- TWO GRAPH ROW ----------
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(id='Graph_NOC_History')
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=8
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(id='Graph_NOC_ER_History')
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=4
                )
            ],
            className="mb-5"
        )

    ],
    fluid=True,
    className="p-4"
)


@callback(
    Output('Graph_ProgramMap','figure'),
    Input('Select_Program','value')
    
)
def Update_Program_Mapping(Program):
    if Program:
        Mapping = Generate_Program_Pathways(Program=Program)
        return Mapping
    else:
        return dash.no_update 

@callback(
    Output('Graph_NOC_History','figure'),
    Output('Graph_NOC_ER_History','figure'),
    Input('Select_NOC','value'),
)
def Update_NOC_History(NOC_Code):
    if NOC_Code:
        NOC_History = Generate_NOC_History_In_Ontario(NOC_GroupingID=NOC_Code)
        NOC_ER_Stats = Generate_NOC_Latest_ER_PCT(NOC_GroupingID=NOC_Code)
        return NOC_History, NOC_ER_Stats
    else:
        return tuple([dash.no_update] * 2)