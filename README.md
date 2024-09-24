# Cosmos Explorer: NASA Data Analysis Hub

## Overview

Cosmos Explorer is an interactive web application that allows users to explore and analyze NASA's vast cosmic datasets. It provides a user-friendly interface for querying space-related information, visualizing data, and uncovering insights about various NASA missions and space phenomena.

## Features

- **Mission Analysis**: Users can input queries about NASA missions, space events, or cosmic phenomena.
- **Dual Analysis Modes**: 
  - Standard Analysis: Quick results using conventional data processing algorithms.
  - Advanced Analysis: In-depth analysis using AI models for more complex queries.
- **Data Visualization**: Interactive charts and graphs to represent analyzed data.
- **Suggested Queries**: Pre-defined suggestions to help users explore the data.
- **Query History**: Keeps track of past queries for easy reference.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## How It Works

1. **User Input**: Users enter their space-related query or select from suggested missions.
2. **Data Processing**: 
   - For standard analysis, the application processes the query using pre-defined algorithms and data sources.
   - For advanced analysis, it utilizes a LLaMA (Large Language Model) to provide more nuanced and detailed responses.
3. **Result Generation**: The system generates textual results and, where applicable, creates data visualizations.
4. **Display**: Results are displayed in an easy-to-read format, with interactive elements for data exploration.

## Technical Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask framework
- **Data Visualization**: Plotly.js
- **AI Model**: LLaMA (for advanced analysis)
- **Database**: [Specify your database, e.g., SQLite, PostgreSQL]

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/nztinversive/NASAdataanalystllm
   cd cosmos-explorer
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add necessary variables (e.g., `DATABASE_URL`, API keys if any)

5. Initialize the database:
   [Add instructions specific to your database setup]

6. Run the application:
   ```
   python main.py
   ```

7. Access the application at `http://localhost:5000`

## Usage

1. Enter a space-related query in the input field.
2. Choose between "Launch Mission" (standard analysis) or "Advanced Launch" (AI-powered analysis).
3. View the results in the Mission Results section.
4. Explore data visualizations if available.
5. Check query history for past searches.

## Contributing

Contributions to Cosmos Explorer are welcome! 




