import pandas as pd
import json
from typing import Union, List, Dict
import plotly.express as px
import plotly.graph_objects as go

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
            fig = px.bar(df, x='Mission', y='Year', 
                         title='NASA Mission Launch Years',
                         labels={'Mission': 'Mission Name', 'Year': 'Launch Year'},
                         color='Status',
                         hover_data=['Description'])
            fig.update_layout(
                yaxis_range=[1960, max(df['Year']) + 5],
                legend_title_text='Mission Status'
            )
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>" +
                              "Launch Year: %{y}<br>" +
                              "Status: %{marker.color}<br>" +
                              "Description: %{customdata[0]}<extra></extra>"
            )
        elif 'status' in query.lower():
            fig = px.pie(df, names='Status', title='Mission Status Distribution')
        else:
            fig = px.scatter(df, x='Year', y='Mission', color='Status', 
                             title='NASA Missions Timeline',
                             labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                             hover_data=['Description'])
        
        chart_json = fig.to_json()
        
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
