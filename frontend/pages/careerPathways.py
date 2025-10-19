from dash import dcc, html, callback ,Input, Output
import dash 

from frontend.DashAppUtils import Get_Program_Options, Generate_Program_Pathways, Get_NOC_Options, Generate_NOC_History_In_Ontario, Generate_NOC_Latest_ER_PCT

dash.register_page(
    __name__,
    path="/careerPathways",
    name="Career Pathways"
    )

layout = html.Div(
    children=[
         html.H2(
                children='Program Career Pathways', style={'textAlign':'left', 'font-size' : '35px', 'font-family':'Courier New'}
            ),
        
        html.Label(children='Select Program',style={'font-size' : '20px', 'margin' : '5px'}),
        dcc.Dropdown(
         id='Select_Program',
         style={'font-size' : '20px', 'margin' : '5px'},
         multi=True,
         options=Get_Program_Options()

        ),

        html.Br(),

        html.Div(
            children=[
                dcc.Graph(
                    id='Graph_ProgramMap'
                )
            ]
        ),

        html.Br(),

        html.Label(children='Select NOC Occupation',style={'font-size' : '20px', 'margin' : '5px'}),
        dcc.Dropdown(
         id='Select_NOC',
         style={'font-size' : '20px', 'margin' : '5px'},
         multi=False,
         options=Get_NOC_Options()

        ),

        html.Br(),

        html.Div(
            style={'display': 'flex', 'justify-content': 'space-between'},
            children=[
            html.Div(
            dcc.Graph(id='Graph_NOC_History'),
            style={'flex': '0 0 70%', 'padding': '10px'}
            ),
            html.Div(
                dcc.Graph(id='Graph_NOC_ER_History'),
                style={'flex': '0 0 30%', 'padding': '10px'}
            )
        ]
        ),

        html.Br(),
        

    ]
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
        NOC_History = Generate_NOC_History_In_Ontario(NOC_Code=NOC_Code)
        NOC_ER_Stats = Generate_NOC_Latest_ER_PCT(NOC_Code=NOC_Code)
        return NOC_History, NOC_ER_Stats
    else:
        return tuple([dash.no_update] * 2)