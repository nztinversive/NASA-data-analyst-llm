import pandas as pd
import json
from typing import Union, List, Dict
import plotly.express as px
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
        
        # Create a single scatter plot
        fig = px.scatter(df, x='Year', y='Mission', 
                         title='NASA Mission Launch Years',
                         labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                         color='Status',
                         hover_data=['Description'],
                         size_max=20)
        
        fig.update_traces(marker=dict(size=12))
        fig.update_layout(
            title=dict(text='NASA Mission Launch Years', font=dict(size=16), x=0.5, xanchor='center'),
            xaxis_title='Launch Year',
            yaxis_title='Mission Name',
            legend_title_text='Mission Status',
            hovermode='closest',
            autosize=True,
            margin=dict(l=50, r=30, t=50, b=50),
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
