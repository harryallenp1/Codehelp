from dash import dcc, html, callback ,Input, Output, dash_table
import dash 
import dash_bootstrap_components as dbc
from UILayer.DashAppUtilities import Get_Program_Options, Get_Post_Grad_Employment_Rate_Measure_Options, Generate_KPI_Comparison


dash.register_page(
    __name__,
    path="/programSearch",
    name="Program Search"
    )


layout = dbc.Container(
    [

        # ---------- PAGE TITLE ----------
        dbc.Row(
            dbc.Col(
                html.H2(
                    "University Program KPI Analysis",
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
                        "Select Program",
                        className="fw-bold mb-2",
                        style={"font-size": "20px"}
                    ),
                    dcc.Dropdown(
                        id='Select_Program',
                        options=Get_Program_Options(),
                        multi=False,
                        className="mb-4"
                    ),

                    html.Label(
                        "Select KPI",
                        className="fw-bold mb-2",
                        style={"font-size": "20px"}
                    ),
                    dcc.Dropdown(
                        id='Select_KPI',
                        options=Get_Post_Grad_Employment_Rate_Measure_Options(),
                        multi=False,
                        className="mb-3"
                    )
                ]
            ),
            className="shadow-sm mb-4"
        ),

        # ---------- TWO KPI GRAPHS ----------
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(id='Graph_KPIMap')
                        ),
                        className="shadow-sm h-100"
                    ),
                    width=6
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(id='Graph_KPIBar')
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
                                 id='Tbl_ProgramKPI',
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
                    width=12
                )
            ],
            className="mb-5"
        )

    ],
    fluid=True,
    className="p-4"
)


@callback(
        Output('Graph_KPIMap', 'figure'),
        Output('Graph_KPIBar', 'figure'),
        Output('Tbl_ProgramKPI','columns'),
        Output('Tbl_ProgramKPI','style_cell'),
        Output('Tbl_ProgramKPI','data'),
        Output('Tbl_ProgramKPI','style_data_conditional'),
        Input('Select_Program','value'),
        Input('Select_KPI','value'),
    )
def Update_KPI_Map(Program, KPI):
    if Program and KPI:
        print(f"Map/Bar Call Back Called")
        Map, Bar, Tbl_Dict = Generate_KPI_Comparison(ProgramID=Program, KPI=KPI)

        if len(Tbl_Dict) == 0:
            return Map, Bar, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        if len(Tbl_Dict) > 0:
            data = Tbl_Dict['Data']
            cols = Tbl_Dict['Cols']
            style = Tbl_Dict['Style']
            styleCond = Tbl_Dict['StyleCond']
            return Map, Bar, cols, style, data, styleCond
    else:
        return tuple([dash.no_update] * 6)