import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import json
import pandas as pd

# Initialize the Dash app with Bootstrap for responsive design
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load the Trackman Data from the file
with open('data/2024-09-15_TrackmanMergedGamePlay.json', 'r') as file:
    trackman_data = json.load(file)

# Convert the JSON data into a DataFrame
df = pd.json_normalize(trackman_data)

# Unique pitcher, team, pitch types, and other data
unique_pitchers = df['pitcher.name'].unique()
unique_teams = df['pitcher.team'].unique()
unique_pitch_types = df['pitchTag.taggedPitchType'].unique()
unique_dates = df['localDateTime'].apply(lambda x: x.split(" ")[0]).unique()  # Extract unique dates

# Helper function to calculate the max width of dropdowns based on longest item
def get_max_width(options):
    """Helper function to get the maximum width (in characters) for dropdown options."""
    return max([len(str(option)) for option in options])

# Layout for the app
app.layout = html.Div([
    # Top bar with logo, search bar, and buttons
    dbc.Row([
        # Left - Navigation Buttons (Air Force and Advanced Scouting)
        dbc.Col([
            dbc.Button("Air Force", id="airforce-btn", className="btn btn-outline-secondary", n_clicks=0,
                       style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none'}),
            dbc.Button("Advanced Scouting", id="scouting-btn", className="btn btn-outline-secondary", n_clicks=0,
                       style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none'})
        ], xs=6, sm=6, md=3, lg=3),  # Responsive widths

        # Center - Logo and Air Force Analytics Text
        dbc.Col([
            html.Div([
                html.Img(src='assets/AF_Logo.svg', height="60px", style={'margin-right': '10px', 'display': 'inline-block'}),
                html.Span("Air Force Analytics", style={'font-size': '2vw', 'font-weight': 'bold', 'vertical-align': 'middle', 'color': '#003087'}),
            ], style={'text-align': 'center', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        ], xs=12, sm=12, md=6, lg=6),  # Responsive widths

        # Right - Search Bar and PDF Button
        dbc.Col([
            dcc.Input(
                placeholder="Search Player Name or Team",
                type="text",
                id="search-bar",
                style={'width': '100%', 'padding': '10px', 'border-radius': '5px', 'border': '1px solid #ced4da'}
            ),
            html.Button("Export to PDF", id="pdf-button", n_clicks=0, className="btn btn-outline-secondary", 
                        style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'margin-left': '10px'}),
        ], xs=12, sm=12, md=3, lg=3, style={'display': 'flex', 'justify-content': 'right'})  # Align search bar and button
    ], style={'padding': '10px', 'background-color': '#f8f9fa'}),

    # Air Force Section with dynamic content
    html.Div(id="dynamic-content", style={'background-color': '#f8f9fa', 'padding': '20px'}),

    # Placeholder for Pitching Filters (This will be displayed when Pitching is clicked)
    html.Div(id="pitching-filter-bar", style={'margin-top': '20px', 'display': 'none'}),

    # Placeholder for generated visualizations
    html.Div(id="visualization-output", style={'text-align': 'center', 'margin-top': '20px'})
])

# Callback to load Air Force Section Buttons with the same style as the main buttons
@app.callback(
    Output('dynamic-content', 'children'),
    [Input('airforce-btn', 'n_clicks')]
)
def display_air_force_content(n_clicks):
    if n_clicks > 0:
        return dbc.Row([
            dbc.Col([
                dbc.Button("Pitching", id="pitching-btn", className="btn btn-outline-secondary", n_clicks=0,
                           style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'width': '150px', 'margin-right': '15px'}),
                dbc.Button("Hitting", id="hitting-btn", className="btn btn-outline-secondary", n_clicks=0,
                           style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'width': '150px', 'margin-right': '15px'}),
                dbc.Button("Catching", id="catching-btn", className="btn btn-outline-secondary", n_clicks=0,
                           style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'width': '150px', 'margin-right': '15px'}),
                dbc.Button("Human Performance", id="performance-btn", className="btn btn-outline-secondary", n_clicks=0,
                           style={'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'width': '200px'})
            ], style={'text-align': 'center', 'margin-top': '20px'})
        ])
    return None

@app.callback(
    [Output('pitching-btn', 'style'),
     Output('pitching-filter-bar', 'children'),
     Output('pitching-filter-bar', 'style')],
    [Input('pitching-btn', 'n_clicks')],
    [State('pitching-btn', 'style')]
)
def display_pitching_filters(n_clicks, pitching_style):
    # Initialize pitching button style if it's None (on first load)
    if pitching_style is None:
        pitching_style = {'background-color': '#f8f9fa', 'color': 'black', 'border': 'none', 'width': '150px'}

    # Check if Pitching button was clicked
    if n_clicks and n_clicks > 0:
        # Update the button's style to make it bold (copy the style to avoid mutating the original)
        new_pitching_style = pitching_style.copy()
        new_pitching_style['font-weight'] = 'bold'

        # Get the dynamic max width for the Pitcher/Team dropdown and Date dropdown
        max_name_width = get_max_width(list(unique_pitchers) + ['Team'])
        max_date_width = get_max_width(unique_dates)

        # Show the filter bar for Pitching with dropdowns and checkboxes
        filter_content = dbc.Row([
            # Dropdown for Pitcher or Team (dynamic width based on longest name)
            dbc.Col([
                dcc.Dropdown(
                    id='pitcher-dropdown',
                    options=[{'label': pitcher, 'value': pitcher} for pitcher in unique_pitchers] + [{'label': 'Team', 'value': 'Team'}],
                    placeholder="Select Pitcher or Team",
                    style={'width': f'{max_name_width}ch'}  # Dynamic width based on the longest name
                )
            ], xs=12, sm=6, md=6, lg=6),

            # Multi-select checkmarks for Bullpen vs. Game
            dbc.Col([
                dcc.Checklist(
                    id='bullpen-game-filter',
                    options=[{'label': 'Bullpen', 'value': 'Bullpen'}, {'label': 'Game', 'value': 'Game'}],
                    value=[],  # Initial value can be empty
                    labelStyle={'display': 'inline-block'},
                    inputStyle={'margin-left': '10px'},  # General input styling
                )
            ], xs=12, sm=6, md=6, lg=6),

            # Checkboxes for each unique pitch type (multiple selections)
            dbc.Col([
                dcc.Checklist(
                    id='pitch-type-filter',
                    options=[{'label': pitch_type, 'value': pitch_type} for pitch_type in unique_pitch_types],
                    value=[],  # Initial value can be empty
                    labelStyle={'display': 'inline-block'},
                    inputStyle={'margin-left': '10px'},  # General input styling
                )
            ], xs=12, sm=6, md=6, lg=6),

            # Checkboxes for LHB/RHB (multiple selections)
            dbc.Col([
                dcc.Checklist(
                    id='lhb-rhb-filter',
                    options=[{'label': 'LHB', 'value': 'LHB'}, {'label': 'RHB', 'value': 'RHB'}],
                    value=[],  # Initial value can be empty
                    labelStyle={'display': 'inline-block'},
                    inputStyle={'margin-left': '10px'},  # General input styling
                )
            ], xs=12, sm=6, md=6, lg=6),


            # Dropdown for selecting one or many dates (dynamic width based on longest date)
            dbc.Col([
                dcc.Dropdown(
                    id='date-dropdown',
                    options=[{'label': date, 'value': date} for date in unique_dates],
                    multi=True,  # Allow multiple dates to be selected
                    placeholder="Select Date(s)",
                    style={'width': f'{max_date_width}ch'}  # Dynamic width based on the longest date
                )
            ], xs=12, sm=6, md=6, lg=6)
        ])

        # Set the style to display the filter bar
        filter_bar_style = {'display': 'block', 'margin-top': '20px'}

        return new_pitching_style, filter_content, filter_bar_style

    # If button is not clicked, return original style and hide the filter bar
    return pitching_style, None, {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
