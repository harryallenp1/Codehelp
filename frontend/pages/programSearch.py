from dash import dcc, html, callback ,Input, Output
import dash 

from frontend.DashAppUtils import Get_Program_Options, Get_Post_Grad_Employment_Rate_Measure_Options, Generate_KPI_Comparison


dash.register_page(
    __name__,
    path="/programSearch",
    name="Program Search"
    )


layout = html.Div(
    children=[
         html.H2(
                children='University Program KPI Analysis', style={'textAlign':'left', 'font-size' : '35px', 'font-family':'Courier New'}
            ),
        
        html.Label(children='Select Program',style={'font-size' : '20px', 'margin' : '5px'}),
        dcc.Dropdown(
         id='Select_Program',
         style={'font-size' : '20px', 'margin' : '5px'},
         multi=False,
         options=Get_Program_Options()

        ),

        html.Label(children='Select KPI',style={'font-size' : '20px', 'margin' : '5px'}),
        dcc.Dropdown(
         id='Select_KPI',
         style={'font-size' : '20px', 'margin' : '5px'},
         multi=False,
         options=Get_Post_Grad_Employment_Rate_Measure_Options()

        ),

        html.Div(
            children=[
                html.Div(children=[
                     dcc.Graph(
                    id='Graph_KPIMap'
                    ),
                ],style={'flex': '1', 'padding': '10px'}
                   
                ),

                html.Div(children=[
                    dcc.Graph(
                    id='Graph_KPIBar',
                    )
                ],style={'flex': '1', 'padding': '10px'}
                    
                ),
            ],style={'display': 'flex', 'flexDirection': 'row'}
        )

        

    ]
)


@callback(
        Output('Graph_KPIMap', 'figure'),
        Output('Graph_KPIBar', 'figure'),
        Input('Select_Program','value'),
        Input('Select_KPI','value'),
    )
def Update_KPI_Map(Program, KPI):
    if Program and KPI:
        print(f"Map/Bar Call Back Called")
        Map, Bar = Generate_KPI_Comparison(Program=Program, KPI=KPI)
        return Map, Bar
    else:
        return tuple([dash.no_update] * 2)