from dash import dcc, html, callback ,Input, Output
import dash 


dash.register_page(
    __name__,
    path="/occupationForecasts",
    name="Future Outcomes"
    )

layout = html.Div(
    children=[
         html.H2(
                children='Forecasts for NOC Occupations', style={'textAlign':'left', 'font-size' : '35px', 'font-family':'Courier New'}
            ),
        


    ]
)