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
            title_font=dict(size=16),  # Set the title font size
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
            hover_data=['ProgramID','Program','UniversityID','University'],
            template='ggplot2'
        )

        bar.update_layout(
            title_font=dict(size=16),  # Set the title font size
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
            # title=f'Career Paths per Program',
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
            # title=f"'{NOC_Occupation}' Employment History in Ontario",
            height=1000,
            template='ggplot2',
        )

        History_Graph.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['Employment (Persons in Thousands)'],
                mode='lines',
                line=dict(color='#172B4A', width=4.5),
                name='Empoyment (Persons in Thousands)',
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
                font_size=15 
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
            ),
            hovermode='x unified',
        )

        return History_Graph
    

    except Exception as e:
        print(f"Generate_NOC_History() => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment History Unavailable'}}
    

def Generate_NOC_ER_Stat(Data, NOC_Occupation):
    try:
        Data = Data.sort_values(by='Monthly PCT', ascending=False)


        Color_Discrete_Map = {
            'Increase':'#186930',
            'No Change':'#183B69',
            'Decrease': '#692618'
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
    


#region Forecast Graphs 

def Generate_Forecast_Graph(Data):
    try:
        
        future_data = Data[Data['set'] == 'Future']
        test_data = Data[Data['set'].isin(['Validation','Test'])]

        line = px.line(
            title='Forecast (2024 - 2029)',
            height=1000,
            template='ggplot2',
        )

        line.add_trace(go.Scatter(
            x=test_data['datestamp'], 
            y=test_data['y'],
            name='Actual',
            line=dict(color='#172B4A', width=4.5),
            mode='lines'
        ))

        line.add_trace(go.Scatter(
            x=future_data['datestamp'], 
            y=future_data['yhat'],
            name='Forecast',
            line=dict(color="#5B160F", width=4.5, dash='dot'),
            mode='lines'
        ))

        line.add_traces(
            go.Scatter(
            x=future_data['datestamp'],
            y=future_data['yhat_upper'],
            mode='lines',
            line=dict(width=0),  
            showlegend=False,
            hoverinfo='skip'
            )
        )

        line.add_traces(
        go.Scatter(
            x=future_data['datestamp'],
            y=future_data['yhat_lower'],
            mode='lines',
            line=dict(width=0), 
            fill='tonexty',      
            fillcolor='rgba(117, 43, 58, 0.2)', 
             hoverinfo='skip',
            name='Forecast Uncertainty Interval'
            )
            )
        


        line.add_trace(go.Scatter(
            x=test_data['datestamp'], 
            y=test_data['yhat'],
            name='Predicted',
            line=dict(color="#2B7561", width=4.5, dash='dash')
        ))

        line.add_traces(
            go.Scatter(
            x=test_data['datestamp'],
            y=test_data['yhat_upper'],
            mode='lines',
            line=dict(width=0),  
            showlegend=False,
            hoverinfo='skip'
            )
        )

        line.add_traces(
        go.Scatter(
            x=test_data['datestamp'],
            y=test_data['yhat_lower'],
            mode='lines',
            line=dict(width=0), 
            fill='tonexty',      
            fillcolor='rgba(43, 117, 97, 0.2)', 
             hoverinfo='skip',
            name='Tested Uncertainty Interval'
            )
            )


        line.update_layout(
            title_font=dict(size=24),  
            font=dict(size=15),  
            hoverlabel=dict(
                font_size=15 
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
            ),
            hovermode='x unified',
        )

        return line





    except Exception as e:
        print(f"Generate_Forecast_Graph() => {e}")
        return {'data': [], 'layout': {'title': f'NOC Employment Forecast Unavailable'}}


#endregion 


#region Simple Visualization Capabilities

def create_simple_line_chart(data, x_col, y_col, title=None, x_label=None, y_label=None):
    """
    Create a simple line chart from data.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title (optional)
        x_label: X-axis label (optional)
        y_label: Y-axis label (optional)
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.line(
            data_frame=data,
            x=x_col,
            y=y_col,
            title=title or f'{y_col} vs {x_col}',
            template='ggplot2',
            height=600
        )
        
        fig.update_layout(
            xaxis_title=x_label or x_col,
            yaxis_title=y_label or y_col,
            font=dict(size=14),
            title_font=dict(size=18)
        )
        
        return fig
    
    except Exception as e:
        print(f"create_simple_line_chart() => {e}")
        return {'data': [], 'layout': {'title': 'Chart Unavailable'}}


def create_simple_bar_chart(data, x_col, y_col, title=None, x_label=None, y_label=None, color_col=None):
    """
    Create a simple bar chart from data.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title (optional)
        x_label: X-axis label (optional)
        y_label: Y-axis label (optional)
        color_col: Column name for color grouping (optional)
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.bar(
            data_frame=data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title or f'{y_col} by {x_col}',
            template='ggplot2',
            height=600
        )
        
        fig.update_layout(
            xaxis_title=x_label or x_col,
            yaxis_title=y_label or y_col,
            font=dict(size=14),
            title_font=dict(size=18)
        )
        
        return fig
    
    except Exception as e:
        print(f"create_simple_bar_chart() => {e}")
        return {'data': [], 'layout': {'title': 'Chart Unavailable'}}


def create_simple_scatter_plot(data, x_col, y_col, title=None, x_label=None, y_label=None, color_col=None, size_col=None):
    """
    Create a simple scatter plot from data.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title (optional)
        x_label: X-axis label (optional)
        y_label: Y-axis label (optional)
        color_col: Column name for color grouping (optional)
        size_col: Column name for marker size (optional)
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.scatter(
            data_frame=data,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col,
            title=title or f'{y_col} vs {x_col}',
            template='ggplot2',
            height=600
        )
        
        fig.update_layout(
            xaxis_title=x_label or x_col,
            yaxis_title=y_label or y_col,
            font=dict(size=14),
            title_font=dict(size=18)
        )
        
        return fig
    
    except Exception as e:
        print(f"create_simple_scatter_plot() => {e}")
        return {'data': [], 'layout': {'title': 'Chart Unavailable'}}


def create_simple_pie_chart(data, values_col, names_col, title=None):
    """
    Create a simple pie chart from data.
    
    Args:
        data: DataFrame containing the data
        values_col: Column name for values
        names_col: Column name for labels
        title: Chart title (optional)
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.pie(
            data_frame=data,
            values=values_col,
            names=names_col,
            title=title or f'{values_col} Distribution',
            template='ggplot2',
            height=600
        )
        
        fig.update_layout(
            font=dict(size=14),
            title_font=dict(size=18)
        )
        
        return fig
    
    except Exception as e:
        print(f"create_simple_pie_chart() => {e}")
        return {'data': [], 'layout': {'title': 'Chart Unavailable'}}


def create_simple_histogram(data, col, title=None, x_label=None, bins=None):
    """
    Create a simple histogram from data.
    
    Args:
        data: DataFrame containing the data
        col: Column name for histogram
        title: Chart title (optional)
        x_label: X-axis label (optional)
        bins: Number of bins (optional)
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.histogram(
            data_frame=data,
            x=col,
            nbins=bins,
            title=title or f'Distribution of {col}',
            template='ggplot2',
            height=600
        )
        
        fig.update_layout(
            xaxis_title=x_label or col,
            yaxis_title='Count',
            font=dict(size=14),
            title_font=dict(size=18)
        )
        
        return fig
    
    except Exception as e:
        print(f"create_simple_histogram() => {e}")
        return {'data': [], 'layout': {'title': 'Chart Unavailable'}}

#endregion


#region Career Pathways Visualizations

def Generate_Occupation_Category_Distribution(Data):
    """
    Create a sunburst chart showing the distribution of occupation categories.
    
    Args:
        Data: DataFrame with occupation hierarchy data
    
    Returns:
        Plotly figure object
    """
    try:
        fig = px.sunburst(
            data_frame=Data,
            path=['Broad Occupation Category', 'Sub-Major Group', 'Unit Group Occupation'],
            title='Occupation Category Distribution',
            height=700,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            font=dict(size=10),
            title_font=dict(size=16),
            hoverlabel=dict(font_size=12)
        )
        
        fig.update_traces(
            textfont=dict(size=8)
        )
        
        # Disable zoom and pan interactions
        fig.update_layout(
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
            dragmode=False
        )
        
        return fig
    
    except Exception as e:
        print(f"Generate_Occupation_Category_Distribution() => {e}")
        return {'data': [], 'layout': {'title': 'Occupation Distribution Unavailable'}}


def Generate_Career_Path_Comparison(Data, NOC_Occupation):
    """
    Create a multi-line comparison chart for different career paths.
    
    Args:
        Data: DataFrame with employment data over time
        NOC_Occupation: Name of the occupation
    
    Returns:
        Plotly figure object
    """
    try:
        fig = go.Figure()
        
        fig.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['Employment (Persons in Thousands)'],
                mode='lines+markers',
                name='Employment',
                line=dict(color='#172B4A', width=3),
                marker=dict(size=6)
            )
        )
        
        fig.update_layout(
            title=f"Career Path Analysis: {NOC_Occupation}",
            xaxis_title='Date',
            yaxis_title='Employment (Thousands)',
            template='ggplot2',
            height=600,
            font=dict(size=12),
            title_font=dict(size=16),
            hovermode='x unified',
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True)
        )
        
        return fig
    
    except Exception as e:
        print(f"Generate_Career_Path_Comparison() => {e}")
        return {'data': [], 'layout': {'title': 'Career Path Comparison Unavailable'}}


def Generate_Regional_Employment_Heatmap(Data):
    """
    Create a heatmap showing employment changes across economic regions.
    
    Args:
        Data: DataFrame with regional employment data
    
    Returns:
        Plotly figure object
    """
    try:
        Data_Sorted = Data.sort_values(by='Monthly PCT', ascending=True)
        
        fig = go.Figure(data=go.Heatmap(
            y=Data_Sorted['Economic Region'],
            z=[Data_Sorted['Monthly PCT']],
            colorscale=[
                [0, '#692618'],
                [0.5, '#183B69'],
                [1, '#186930']
            ],
            showscale=True,
            hovertemplate='Region: %{y}<br>Change: %{z:.2f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Regional Employment Change Heatmap',
            xaxis_title='',
            yaxis_title='Economic Region',
            height=600,
            template='ggplot2',
            font=dict(size=12),
            title_font=dict(size=16),
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True)
        )
        
        return fig
    
    except Exception as e:
        print(f"Generate_Regional_Employment_Heatmap() => {e}")
        return {'data': [], 'layout': {'title': 'Regional Heatmap Unavailable'}}


def Generate_Program_Occupation_Network(Data):
    """
    Create a network-style visualization showing program-occupation connections.
    
    Args:
        Data: DataFrame with program and occupation mappings
    
    Returns:
        Plotly figure object
    """
    try:
        # Create a hierarchical treemap with better styling
        fig = px.treemap(
            data_frame=Data,
            path=['Program', 'Broad Occupation Category', 'Sub-Major Group'],
            title='Program to Occupation Network',
            height=700,
            color='Broad Occupation Category',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(
            marker=dict(
                line=dict(color='white', width=2)
            ),
            textfont=dict(size=16)
        )
        
        fig.update_layout(
            font=dict(size=12),
            title_font=dict(size=16),
            hoverlabel=dict(font_size=12)
        )
        
        fig.update_traces(
            textfont=dict(size=10)
        )
        
        return fig
    
    except Exception as e:
        print(f"Generate_Program_Occupation_Network() => {e}")
        return {'data': [], 'layout': {'title': 'Program-Occupation Network Unavailable'}}


def Generate_Employment_Trend_Summary(Data):
    """
    Create a summary visualization with key employment metrics.
    
    Args:
        Data: DataFrame with employment statistics
    
    Returns:
        Plotly figure object
    """
    try:
        fig = go.Figure()
        
        # Add employment line
        fig.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['Employment (Persons in Thousands)'],
                mode='lines',
                name='Employment',
                line=dict(color='#172B4A', width=3),
                fill='tozeroy',
                fillcolor='rgba(23, 43, 74, 0.1)'
            )
        )
        
        # Add moving average
        fig.add_trace(
            go.Scatter(
                x=Data['ds'],
                y=Data['3-Month Moving Average'],
                mode='lines',
                name='3-Month Average',
                line=dict(color='#9D3D39', width=2, dash='dash')
            )
        )
        
        fig.update_layout(
            title='Employment Trend Summary',
            xaxis_title='Date',
            yaxis_title='Employment (Thousands)',
            template='ggplot2',
            height=500,
            font=dict(size=12),
            title_font=dict(size=16),
            hovermode='x unified',
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.25,
                xanchor='center',
                x=0.5
            )
        )
        
        return fig
    
    except Exception as e:
        print(f"Generate_Employment_Trend_Summary() => {e}")
        return {'data': [], 'layout': {'title': 'Employment Trend Summary Unavailable'}}

#endregion