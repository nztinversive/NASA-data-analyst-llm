import pandas as pd
import json
from typing import Union, List, Dict
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
        # Sample DataFrame (in a real-world scenario, this would be replaced with actual data)
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
            ],
            'Duration': ['8 days', '10+ years', '30+ years', '45+ years', '20 years'],
            'Key Achievements': [
                'First human on the Moon',
                'Discovery of ancient riverbeds on Mars',
                'Deep field images of the universe',
                'First human-made object to leave the solar system',
                'Discovery of ocean worlds on Saturn\'s moons'
            ]
        }
        df = pd.DataFrame(data)
        
        # Process the query
        if 'mission' in query.lower():
            result = df['Mission'].tolist()
        elif 'year' in query.lower():
            result = df['Year'].tolist()
        elif 'status' in query.lower():
            result = df['Status'].tolist()
        else:
            result = df.to_dict(orient='records')
        
        # Create scatter plot
        scatter_fig = px.scatter(df, x='Year', y='Mission', 
                                 title='NASA Mission Launch Years',
                                 labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                                 color='Status',
                                 hover_data=['Description', 'Duration', 'Key Achievements'],
                                 size_max=20)
        
        scatter_fig.update_traces(marker=dict(size=12))
        scatter_fig.update_layout(
            title=dict(text='NASA Mission Launch Years', font=dict(size=16), x=0.5, xanchor='center'),
            xaxis_title='Launch Year',
            yaxis_title='Mission Name',
            legend_title_text='Mission Status',
            hovermode='closest',
            dragmode='pan',
            xaxis=dict(
                rangeslider=dict(visible=True),
                type='linear'
            )
        )
        
        # Create bar chart
        df['Decade'] = (df['Year'] // 10) * 10
        missions_per_decade = df.groupby('Decade').size().reset_index(name='Count')
        bar_fig = px.bar(missions_per_decade, x='Decade', y='Count',
                         title='NASA Missions per Decade',
                         labels={'Decade': 'Decade', 'Count': 'Number of Missions'})
        
        bar_fig.update_layout(
            title=dict(text='NASA Missions per Decade', font=dict(size=16), x=0.5, xanchor='center'),
            xaxis_title='Decade',
            yaxis_title='Number of Missions',
            dragmode='pan'
        )
        
        # Combine both charts
        fig = make_subplots(rows=2, cols=1, subplot_titles=('NASA Mission Launch Years', 'NASA Missions per Decade'))
        for trace in scatter_fig.data:
            fig.add_trace(trace, row=1, col=1)
        for trace in bar_fig.data:
            fig.add_trace(trace, row=2, col=1)
        
        fig.update_layout(height=1000, showlegend=True, hovermode='closest')
        
        # Add reset zoom button
        fig.update_layout(
            updatemenus=[
                dict(
                    type="button",
                    direction="left",
                    buttons=[
                        dict(
                            args=[{"xaxis.range": None, "yaxis.range": None}],
                            label="Reset Zoom",
                            method="relayout"
                        )
                    ],
                    pad={"r": 10, "t": 10},
                    showactive=False,
                    x=0.11,
                    xanchor="left",
                    y=1.1,
                    yanchor="top"
                )
            ]
        )
        
        chart_json = json.dumps(fig.to_dict(), default=serialize_numpy)
        
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
