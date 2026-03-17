from dash import dcc, html, callback ,Input, Output
import dash 
import dash_bootstrap_components as dbc

from UILayer.DashAppUtilities import (
    Get_Program_Options, 
    Get_NOC_Options, 
    Generate_Program_Pathways, 
    Generate_NOC_History_In_Ontario, 
    Generate_NOC_Latest_ER_PCT,
    Generate_Occupation_Distribution,
    Generate_Regional_Heatmap,
    Generate_Employment_Summary,
    Generate_STL_Decomposition_Chart
)

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
            className="mb-4"
        ),

        # ---------- ADDITIONAL VISUALIZATIONS ROW ----------
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Occupation Distribution", className="mb-3"),
                                dcc.Graph(id='Graph_Occupation_Distribution')
                            ]
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Regional Employment Heatmap", className="mb-3"),
                                dcc.Graph(id='Graph_Regional_Heatmap')
                            ]
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=6
                )
            ],
            className="mb-4"
        ),

        # ---------- EMPLOYMENT SUMMARY ROW ----------
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Employment Trend Summary", className="mb-3"),
                            dcc.Graph(id='Graph_Employment_Summary')
                        ]
                    ),
                    className="shadow-sm"
                ),
                width=12
            ),
            className="mb-4"
        ),

        # ---------- STL DECOMPOSITION ROW ----------
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("STL Decomposition Analysis", className="mb-3"),
                            dcc.Graph(id='Graph_STL_Decomposition')
                        ]
                    ),
                    className="shadow-sm"
                ),
                width=12
            ),
            className="mb-5"
        )

    ],
    fluid=True,
    className="p-4"
)


@callback(
    Output('Graph_ProgramMap','figure'),
    Output('Graph_Occupation_Distribution','figure'),
    Input('Select_Program','value')
    
)
def Update_Program_Mapping(Program):
    if Program:
        Mapping = Generate_Program_Pathways(Program=Program)
        Distribution = Generate_Occupation_Distribution(Program=Program)
        return Mapping, Distribution
    else:
        return tuple([dash.no_update] * 2)

@callback(
    Output('Graph_NOC_History','figure'),
    Output('Graph_NOC_ER_History','figure'),
    Output('Graph_Regional_Heatmap','figure'),
    Output('Graph_Employment_Summary','figure'),
    Output('Graph_STL_Decomposition','figure'),
    Input('Select_NOC','value'),
)
def Update_NOC_History(NOC_Code):
    if NOC_Code:
        NOC_History = Generate_NOC_History_In_Ontario(NOC_GroupingID=NOC_Code)
        NOC_ER_Stats = Generate_NOC_Latest_ER_PCT(NOC_GroupingID=NOC_Code)
        Regional_Heatmap = Generate_Regional_Heatmap(NOC_GroupingID=NOC_Code)
        Employment_Summary = Generate_Employment_Summary(NOC_GroupingID=NOC_Code)
        STL_Decomposition = Generate_STL_Decomposition_Chart(NOC_GroupingID=NOC_Code)
        return NOC_History, NOC_ER_Stats, Regional_Heatmap, Employment_Summary, STL_Decomposition
    else:
        return tuple([dash.no_update] * 5)