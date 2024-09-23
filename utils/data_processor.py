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
            result = json.loads(df.to_json(orient='records'))
        
        # Create visualizations
        figs = []
        
        # Scatter plot with time range selector
        scatter_fig = px.scatter(df, x='Year', y='Mission', 
                         title='NASA Mission Launch Years',
                         labels={'Year': 'Launch Year', 'Mission': 'Mission Name'},
                         color='Status',
                         hover_data=['Description'],
                         size_max=20)
        scatter_fig.update_traces(marker=dict(size=12), visible=True)
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
        scatter_fig.update_traces(
            hovertemplate="<b>%{y}</b><br>" +
                          "Launch Year: %{x}<br>" +
                          "Status: %{marker.color}<br>" +
                          "Description: %{customdata[0]}<extra></extra>"
        )
        figs.append(scatter_fig)
        
        # Bar chart: Mission count by status
        status_counts = df['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        bar_fig = px.bar(status_counts, x='Status', y='Count',
                         title='Mission Count by Status',
                         labels={'Status': 'Mission Status', 'Count': 'Number of Missions'},
                         color='Status')
        bar_fig.update_traces(visible=False)
        bar_fig.update_layout(
            title=dict(text='Mission Count by Status', font=dict(size=16), x=0.5, xanchor='center'),
            xaxis_title='Mission Status',
            yaxis_title='Number of Missions'
        )
        bar_fig.update_traces(
            hovertemplate="Status: %{x}<br>Number of Missions: %{y}<extra></extra>"
        )
        figs.append(bar_fig)
        
        # Enhanced pie chart for mission status
        pie_fig = px.pie(df, names='Status', title='Mission Status Distribution',
                         hover_data=['Mission'], hole=0.3)
        pie_fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>" +
                          "Percentage: %{percent}<br>" +
                          "Missions: %{customdata}<extra></extra>",
            visible=False
        )
        pie_fig.update_layout(
            title=dict(text='Mission Status Distribution', font=dict(size=16), x=0.5, xanchor='center'),
            uniformtext_minsize=12,
            uniformtext_mode='hide'
        )
        figs.append(pie_fig)
        
        # Mission timeline
        timeline_fig = px.timeline(df, x_start='Year', x_end='Year', y='Mission', color='Status',
                                   hover_name='Mission', hover_data=['Description'])
        timeline_fig.update_yaxes(autorange="reversed")
        timeline_fig.update_traces(visible=False)
        timeline_fig.update_layout(
            title=dict(text='NASA Missions Timeline', font=dict(size=16), x=0.5, xanchor='center'),
            xaxis_title='Year',
            yaxis_title='Mission',
            legend_title_text='Mission Status'
        )
        figs.append(timeline_fig)
        
        # Create updatemenus for chart type selection
        updatemenus = [
            dict(
                type="buttons",
                direction="right",
                x=0.1,
                y=1.15,
                showactive=True,
                buttons=[
                    dict(label="Scatter Plot",
                         method="update",
                         args=[{"visible": [True, False, False, False]},
                               {"title": "NASA Mission Launch Years"}]),
                    dict(label="Bar Chart",
                         method="update",
                         args=[{"visible": [False, True, False, False]},
                               {"title": "Mission Count by Status"}]),
                    dict(label="Pie Chart",
                         method="update",
                         args=[{"visible": [False, False, True, False]},
                               {"title": "Mission Status Distribution"}]),
                    dict(label="Timeline",
                         method="update",
                         args=[{"visible": [False, False, False, True]},
                               {"title": "NASA Missions Timeline"}])
                ]
            )
        ]
        
        # Make all charts responsive and add updatemenus
        for fig in figs:
            fig.update_layout(
                autosize=True,
                margin=dict(l=30, r=30, t=50, b=30),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                updatemenus=updatemenus
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
