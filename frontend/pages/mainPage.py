from dash import dcc, html, callback ,Input, Output
import dash 

dash.register_page(
    __name__,
    path="/",
    name="Home"
    )

layout = html.Div(
    children=[
            html.Div(
                children=[
                       dcc.Link(
                            children=[
                            html.Img(src='/assets/icons/learning.png', style={'width':'300px', 'height':'300px'}),
                        ],
                        className='main-page-1-1 circle-container',
                        href='/careerPathways',
                        ),
                        dcc.Link(
                            children=[
                            html.Img(src='/assets/icons/trend.png', style={'width':'300px', 'height':'300px'}),
                        ],
                        className='main-page-2-2 circle-container',
                        href='/occupationForecasts', 
                        ),
                        dcc.Link(
                            children=[
                            html.Img(src='/assets/icons/magnifier.png', style={'width':'300px', 'height':'300px'}),
                        ],
                        className='main-page-3-1 circle-container',
                        href='/programSearch',                         
                        ),
        
                ],
                className='main_page_grid'
            ),
    ]
)