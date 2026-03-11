from dash import dcc, html, callback ,Input, Output, dash_table
import dash 
import dash_bootstrap_components as dbc

from UILayer.DashAppUtilities import (Get_NOC_Options, Get_Province_Options, Generate_Forecast_Analysis)


dash.register_page(
    __name__,
    path="/occupationForecasts",
    name="Future Outcomes"
    )

layout = dbc.Container(
    [

        # ---------- PAGE TITLE ----------
        dbc.Row(
            dbc.Col(
                html.H2(
                    "Future Outcomes",
                    className="text-start mt-3 mb-4",
                    style={"font-size": "35px"}
                ),
                width=12
            )
        ),

        # ---------- PROGRAM + KPI SELECTORS ----------
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label(
                        "Select Province",
                        className="fw-bold mb-2",
                        style={"font-size": "20px"}
                    ),
                    dcc.Dropdown(
                        id='Select_Province',
                        options=Get_Province_Options(),
                        multi=False,
                        className="mb-4"
                    ),

                    html.Label(
                        "Select NOC Occupation Group",
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
                            dcc.Graph(id='Graph_NOC_Prov_Forecast')
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                             html.Div(
                                 
                             
                             dash_table.DataTable(
                                 id='Tbl_Forecast',
                                sort_action='native',
                                sort_mode='multi',
                                style_cell={'textAlign': 'left'},  
                                style_table={'height': '500px', 'overflowY': 'auto'},
                                column_selectable="multi",
                                selected_rows=[],
                                filter_action='native',
                                fixed_rows={'headers': True},
                                fixed_columns={'headers': True}
            
                            ), className='dbc dbc-row-selectable'),
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=6
                )

               
            ],
            className="mb-5"
        )

      

    ],
    fluid=True,
    className="p-4"
)



@callback(
        Output('Graph_NOC_Prov_Forecast', 'figure'),
        Output('Tbl_Forecast','columns'),
        Output('Tbl_Forecast','style_cell'),
        Output('Tbl_Forecast','data'),
        Output('Tbl_Forecast','style_data_conditional'),
        Input('Select_Province','value'),
        Input('Select_NOC','value'),
    )
def Update_Graph_Forecasts(provinceid, noc_groupingid):
    if provinceid and noc_groupingid:
        graph, Tbl_Dict = Generate_Forecast_Analysis(provinceid=provinceid, noc_groupingid=noc_groupingid)
        
        if len(Tbl_Dict) == 0:
            return graph, tuple([dash.no_update] * 4)
        
        if len(Tbl_Dict) > 0:
            data = Tbl_Dict['Data']
            cols = Tbl_Dict['Cols']
            style = Tbl_Dict['Style']
            styleCond = Tbl_Dict['StyleCond']
            return graph, cols, style, data, styleCond

    else:
        return tuple([dash.no_update] * 5)