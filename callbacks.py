from dash.dependencies import Input, Output
from components.pitchZoneViz import generate_pitch_plot
from dash import dcc, html

def register_callbacks(app, df):
    @app.callback(
        Output('visualization-output', 'children'),
        Input('pitcher-dropdown', 'value')
    )
    def update_visualization(pitcher):
        if pitcher:
            image_src = generate_pitch_plot(pitcher, df)
            return html.Img(src=image_src, style={'width': '600px', 'height': '800px'})
        return html.Div("Select a pitcher to generate a visualization.", style={'color': '#003087'})
