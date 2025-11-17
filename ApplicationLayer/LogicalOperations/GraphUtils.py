#By: Abira Esther Demello
#Graphing the Data 

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

        return scatter_map


    except Exception as e:
         print(f"Graph_Program_University_Post_Grad_Employment_Rate_Map() => {e}")
         return {'data': [], 'layout': {'title': f'Post-Grad Employment Rate Data Unavailable for {Program} Map'}}