'''
This module allows us to create graph object and pass it on to the frontend dashboard for visualization.
'''


print('Importing GraphUtils\n')

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


def Graph_Program_University_Post_Grad_Employment_Rate_Map(Program, Measure, Data):
    try:
        scatter_map = px.scatter_map(
            title=f'{Program} - {Measure} Mapped by University',
            data_frame=Data,
            lat='Lat',
            lon='Lon',
            height=900,
            size=Measure,
            color=Measure,
            color_continuous_scale=['#692618','#183B69','#186930'],
            text='University',
            hover_data=['ProgramID','Program','UniversityID','University']
        )

        scatter_map.update_layout(
            title_font=dict(size=24),  # Set the title font size
            font=dict(size=15),  # Set general font size for labels and axis titles
            hoverlabel=dict(
                font_size=20  # Set font size for hover data
            ),
            xaxis=dict(
                title_font=dict(size=18),  # Set x-axis title font size
                tickfont=dict(size=12)  # Set x-axis tick font size
            ),
            yaxis=dict(
                title_font=dict(size=18),  # Set y-axis title font size
                tickfont=dict(size=12)  # Set y-axis tick font size
            ),
            mapbox=dict(
                center=dict(lat=Data['Lat'].mean(), lon=Data['Lon'].mean()),  # Center the map on the data
                zoom=9,  # Set a zoom level that shows both primary and secondary points
  
            ),
            coloraxis_showscale=False
        )

        del Data

        # pio.write_html(scatter_map, 'Check.html',auto_open=True)

        return scatter_map


    except Exception as e:
         print(f"Graph_Program_University_Post_Grad_Employment_Rate_Map() => {e}")
         return {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {Program} Map'}}


def Graph_Program_University_Post_Grad_Employment_Rate_Bar(Program, Measure, Data):
    try:

        # print(Measure)
        Data = Data.sort_values(by=Measure, ascending=False)
        bar = px.bar(
            title=f'{Program} - {Measure} Comparison by University',
            data_frame=Data,
            x='University',
            y=Measure,
            height=900,
            color=Measure,
            color_continuous_scale=['#692618','#183B69','#186930'],
            # text='University',
            hover_data=['ProgramID','Program','UniversityID','University']
        )

        bar.update_layout(
            title_font=dict(size=24),  # Set the title font size
            font=dict(size=15),  # Set general font size for labels and axis titles
            hoverlabel=dict(
                font_size=20  # Set font size for hover data
            ),
            xaxis=dict(
                title_font=dict(size=18),  # Set x-axis title font size
                tickfont=dict(size=12)  # Set x-axis tick font size
            ),
            yaxis=dict(
                title_font=dict(size=18),  # Set y-axis title font size
                tickfont=dict(size=12)  # Set y-axis tick font size
            ),
            coloraxis_showscale=False
        )

        return bar

    

    except Exception as e:
        print(f"Graph_Program_University_Post_Grad_Employment_Rate_Bar() => {e}")
        return {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {Program} Bar'}}


def Generate_Program_to_Occupation_Mapping(Data):
    try:

        Mappings = px.treemap(
            title=f'Career Paths per Program',
            data_frame=Data,
            path=['Program','Broad Occupation Category','Sub-Major Group','Unit Group Occupation'],
            height=900,
            template='ggplot2',
            color_discrete_sequence=['white'],
            
            
            
        )
        Mappings.update_traces(
            marker=dict(
            line=dict(color="#1F5896", width=2),
            colorscale=None,
            cmin=None,
            cmax=None
                ),
            hovertemplate=''
        )

        Mappings.update_layout(
             font=dict(
        size=18,                
        ),
            title=dict(
        font=dict(size=28),
        x=0.5
        ),
         hoverlabel=dict(
                font_size=20 
            ),

        )

        del Data
        
        return Mappings
    
    

    except Exception as e:
        print(f"Generate_Program_to_Occupation_Mapping() => {e}")
        return {'data': [], 'layout': {'title': f'Program-Occupation Mappings Unavailable'}}
    

def Generate_NOC_History(Data, NOC_Occupation):
    try:
        History_Graph = px.line(
            title=f"'{NOC_Occupation}' Employment History in Ontario",
            height=1000,
            template='ggplot2'
        )

        History_Graph.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['Employment (Persons in Thousands)'],
                mode='lines',
                line=dict(color='#172B4A', width=4.5),
                name='Empoyment (Persons in Thousands)'
            )
        )

        History_Graph.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['3-Month Moving Average'],
                mode='lines',
                line=dict(color="#9D3D39", width=4.5, dash='dash'),
                name='Quarterly Moving Average'
            )
        )

        History_Graph.add_traces(
            go.Scatter(
            x=Data['ds'],
            y=Data['Upper Band'],
            mode='lines',
            line=dict(width=0),  
            showlegend=False,
            hoverinfo='skip'
            )
        )

        History_Graph.add_traces(
        go.Scatter(
            x=Data['ds'],
            y=Data['Lower Band'],
            mode='lines',
            line=dict(width=0), 
            fill='tonexty',      
            fillcolor='rgba(219, 118, 119, 0.2)', 
             hoverinfo='skip',
            name='Employment Volatility'
            )
            )



        History_Graph.update_layout(
            title_font=dict(size=24),  
            font=dict(size=15),  
            hoverlabel=dict(
                font_size=20  
            ),
            xaxis=dict(
                title='Date (Monthly)',
                title_font=dict(size=20),  
                tickfont=dict(size=18)  
            ),
            yaxis=dict(
                title='Employment (Persons in Thousands)',
                title_font=dict(size=20),  
                tickfont=dict(size=18)  
            ),
             legend=dict(
                orientation='h',       
                yanchor='bottom',     
                y=-0.3,               
                xanchor='center',      
                 x=0.5,                 
                font=dict(size=16)     
            )
        )

        return History_Graph
    

    except Exception as e:
        print(f"Generate_NOC_History() => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History Unavailable'}}


def Generate_NOC_ER_Stat(Data, NOC_Occupation):
    try:
        Data = Data.sort_values(by='Monthly PCT', ascending=False)


        Color_Discrete_Map = {
            'Lift':'#186930',
            'No Change':'#183B69',
            'Drop': '#692618'
        }

        Bar = px.bar(
            height=1000,
            template='ggplot2',
            data_frame=Data,
            y='Economic Region',
            x='Monthly PCT',
            text='Monthly PCT',
            color='Change',
            color_discrete_map=Color_Discrete_Map,
        )

        Bar.update_layout(
            title_font=dict(size=24),  
            font=dict(size=15),  
            hoverlabel=dict(
                font_size=20  
            ),
            xaxis=dict(
                title='Employment Change as %',
                title_font=dict(size=20),  
                tickfont=dict(size=18)  
            ),
            yaxis=dict(
                title='Economic Regions in Ontario',
                title_font=dict(size=20),  
                tickfont=dict(size=18)  
            ),
             legend=dict(
                orientation='h',      
                yanchor='bottom',      
                y=-0.3,                
                xanchor='center',      
                 x=0.5,                 
                font=dict(size=16)     
            )
        )

        return Bar

    except Exception as e:
        print(f"Generate_NOC_ER_Stat() => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History for ERs Unavailable'}}