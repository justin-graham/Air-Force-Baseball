import dash
import base64
from dash import dcc, html
import dash_bootstrap_components as dbc
from callbacks import register_callbacks
from components.pitchZoneViz import generate_pitch_plot  # Correct import
import json
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Encode the logo image to base64
logo = 'assets/AF_Logo.png'
logo_base64 = base64.b64encode(open(logo, 'rb').read()).decode('ascii')

# Load the Trackman Data from the file
with open('data/2024-09-15_TrackmanMergedGamePlay.json', 'r') as file:
    trackman_data = json.load(file)

# Convert the JSON data into a DataFrame
df = pd.json_normalize(trackman_data)

# Unique pitcher and team data
unique_pitchers = df['pitcher.name'].unique()
unique_teams = df['pitcher.team'].unique()

# Layout for the app
app.layout = html.Div([
    # Top bar with logo, search bar, and buttons
    dbc.Row([
        # Left - Navigation Buttons (Air Force and Advanced Scouting)
        dbc.Col([
            dbc.Button("Air Force", id="airforce-btn", className="btn btn-outline-secondary", n_clicks=0,
                       style={'width': '150px', 'margin-right': '15px', 'background-color': '#f8f9fa', 'color': 'black', 'border': 'none'}),
            dbc.Button("Advanced Scouting", id="scouting-btn", className="btn btn-outline-secondary", n_clicks=0,
                       style={'width': '180px', 'background-color': '#f8f9fa', 'color': 'black', 'border': 'none'})
        ], width=3),

        # Center - Logo and Air Force Analytics Text
        dbc.Col([
            html.Div([
                html.Img(src='data:image/png;base64,{}'.format(logo_base64), height="60px", style={'vertical-align': 'middle', 'margin-right': '10px'}),
                html.Span("Air Force Analytics", style={'font-size': '28px', 'font-weight': 'bold', 'vertical-align': 'middle', 'color': '#003087'}),
            ], style={'text-align': 'center', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        ], width=6),

        # Right - Search Bar and PDF Button
        dbc.Col([
            dcc.Input(
                placeholder="Search Player Name or Team",
                type="text",
                id="search-bar",
                style={'width': '70%', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ced4da', 'margin-right': '10px'}
            ),
            html.Button("Export to PDF", id="pdf-button", n_clicks=0, className="btn btn-outline-secondary", style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none'}),
        ], width=3, style={'text-align': 'right'})
    ], style={'padding': '10px', 'background-color': '#f8f9fa'}),

    # Air Force Section with filter for pitchers
    html.Div(id="dynamic-content", style={'background-color': '#f8f9fa', 'padding': '20px'}),
    
    # Filter for pitchers and teams
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pitcher-dropdown',
                options=[{'label': pitcher, 'value': pitcher} for pitcher in unique_pitchers],
                placeholder="Select Pitcher",
                style={'width': '100%'}
            )
        ], width=6),
        
        dbc.Col([
            dcc.Dropdown(
                id='team-dropdown',
                options=[{'label': team, 'value': team} for team in unique_teams],
                placeholder="Select Team",
                style={'width': '100%'}
            )
        ], width=6)
    ], justify="center", style={'margin-top': '20px'}),
    
    # Placeholder for generated visualizations
    html.Div(id="visualization-output", style={'text-align': 'center', 'margin-top': '20px'})
])

# Register callbacks
register_callbacks(app, df)

if __name__ == '__main__':
    app.run_server(debug=True)
