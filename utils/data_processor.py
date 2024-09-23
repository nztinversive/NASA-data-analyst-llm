import pandas as pd
import json
from typing import Union, List, Dict

def process_query(query: str) -> Union[List, Dict]:
    try:
        # This is a placeholder function. In a real-world scenario, you would
        # implement more complex data processing logic here.
        
        # For demonstration purposes, we'll create a sample DataFrame
        data = {
            'Mission': ['Apollo 11', 'Mars Rover', 'Hubble Telescope'],
            'Year': [1969, 2012, 1990],
            'Status': ['Completed', 'Ongoing', 'Ongoing']
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
        
        return result
    except Exception as e:
        error_message = f"An error occurred while processing the query: {str(e)}"
        return {"error": error_message}

def get_query_suggestions() -> List[str]:
    return [
        "List all missions",
        "Show mission years",
        "Display mission statuses",
        "Provide all mission data"
    ]
