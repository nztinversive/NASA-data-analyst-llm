import pandas as pd
import json
from typing import Union, List, Dict
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def serialize_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.void):
        return None
    return obj

def process_query(query: str) -> Union[List, Dict]:
    try:
        # This is a placeholder function. In a real-world scenario, you would
        # implement more complex data processing logic here.
        
        # For demonstration purposes, we'll create a sample DataFrame
        data = {
            'Mission': ['Apollo 11', 'Mars Rover', 'Hubble Telescope', 'Voyager 1', 'Cassini'],
            'Year': [1969, 2012, 1990, 1977, 1997],
            'Status': ['Completed', 'Ongoing', 'Ongoing', 'Ongoing', 'Completed'],
            'Description': [
                'First manned mission to land on the Moon',
                'Exploration of Mars surface',
                'Space telescope for deep space observation',
                'Interstellar space probe',
                'Exploration of Saturn and its moons'
            ]
        }
        df = pd.DataFrame(data)
        
        # Process the query (this is a simplified example)
        if 'mission' in query.lower():
            result = df['Mission'].tolist()
        elif 'year' in query.lower():
            result = df['Year'].tolist()
        elif 'status' in query.lower():
            result = df['Status'].tolist()
        else:
            result = json.loads(df.to_json(orient='records'))
        
        # Create visualization
        if 'year' in query.lower():
            # Scatter plot
            scatter_fig = px.scatter(df, x='Year', y='Mission', 
                             title='NASA Mission Launch Years',
                             labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                             color='Status',
                             hover_data=['Description'],
                             size_max=20)
            scatter_fig.update_traces(marker=dict(size=12))
            scatter_fig.update_layout(
                title=dict(
                    text='NASA Mission Launch Years',
                    font=dict(size=16),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis_title='Launch Year',
                yaxis_title='Mission Name',
                legend_title_text='Mission Status',
                margin=dict(l=50, r=50, t=50, b=50),
                hovermode='closest',
                dragmode='pan',
                xaxis=dict(
                    rangeslider=dict(visible=True),
                    type='linear'
                ),
                autosize=True,
                xaxis_title_font_size=12,
                yaxis_title_font_size=12,
                legend_font_size=10,
                height=None,  # Remove fixed height
                font=dict(size=10),  # Reduce font size for better mobile display
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)  # Move legend to top
            )
            scatter_fig.update_traces(
                hovertemplate="<b>%{y}</b><br>" +
                              "Launch Year: %{x}<br>" +
                              "Status: %{marker.color}<br>" +
                              "Description: %{customdata[0]}<extra></extra>"
            )
            
            # Bar chart
            df['Decade'] = (df['Year'] // 10) * 10
            missions_per_decade = df.groupby('Decade').size().reset_index(name='Count')
            bar_fig = px.bar(missions_per_decade, x='Decade', y='Count',
                             title='Number of NASA Missions per Decade',
                             labels={'Decade': 'Decade', 'Count': 'Number of Missions'},
                             hover_data=['Count'])
            bar_fig.update_layout(
                title=dict(
                    text='Number of NASA Missions per Decade',
                    font=dict(size=16),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis_title='Decade',
                yaxis_title='Number of Missions',
                margin=dict(l=50, r=50, t=50, b=50),
                autosize=True,
                xaxis_title_font_size=12,
                yaxis_title_font_size=12,
                legend_font_size=10,
                font=dict(size=10)
            )
            bar_fig.update_traces(
                hovertemplate="Decade: %{x}<br>Number of Missions: %{y}<extra></extra>"
            )
            
            figs = [scatter_fig, bar_fig]
        elif 'status' in query.lower():
            fig = px.pie(df, names='Status', title='Mission Status Distribution', hover_data=['Mission'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                title=dict(
                    text='Mission Status Distribution',
                    font=dict(size=16),
                    x=0.5,
                    xanchor='center'
                ),
                autosize=True,
                legend_font_size=10,
                font=dict(size=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Rockwell")
            )
            figs = [fig]
        else:
            fig = px.scatter(df, x='Year', y='Mission', color='Status', 
                             title='NASA Missions Timeline',
                             labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                             hover_data=['Description'])
            fig.update_layout(
                title=dict(
                    text='NASA Missions Timeline',
                    font=dict(size=16),
                    x=0.5,
                    xanchor='center'
                ),
                autosize=True,
                xaxis_title_font_size=12,
                yaxis_title_font_size=12,
                legend_font_size=10,
                font=dict(size=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            figs = [fig]
        
        # Make the charts responsive
        for fig in figs:
            fig.update_layout(
                autosize=True,
                margin=dict(l=30, r=30, t=50, b=30),  # Reduce margins for mobile
            )
        
        result = json.loads(json.dumps(result, default=serialize_numpy))
        chart_json = json.dumps([fig.to_dict() for fig in figs], default=serialize_numpy)
        
        return {'data': result, 'chart': chart_json}
    except Exception as e:
        error_message = f"An error occurred while processing the query: {str(e)}"
        return {"error": error_message}

def get_query_suggestions() -> List[str]:
    return [
        "List all missions",
        "Show mission launch years",
        "Display mission statuses",
        "Provide all mission data"
    ]
