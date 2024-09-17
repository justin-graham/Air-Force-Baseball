import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def generate_pitch_plot(pitcher, df):
    # Filter data for the selected pitcher
    pitcher_data = df[df['pitcher.name'] == pitcher]
    
    # Create the plot
    plt.figure(figsize=(6, 8))
    sns.scatterplot(
        data=pitcher_data,
        x='pitch.location.plateLocSide',
        y='pitch.location.plateLocHeight',
        hue='pitchTag.taggedPitchType',
        palette={'Fastball': 'red', 'Slider': 'green', 'Splitter': 'purple', 'ChangeUp': '#FFD700'},
        s=100,
        marker='o',
        legend=False
    )

    # Define strike zone
    strike_zone = {'top': 3.5, 'bottom': 1.5, 'left': -0.71, 'right': 0.71}
    plt.plot([strike_zone['left'], strike_zone['right']], [strike_zone['top'], strike_zone['top']], color='black')
    plt.plot([strike_zone['left'], strike_zone['right']], [strike_zone['bottom'], strike_zone['bottom']], color='black')
    plt.plot([strike_zone['left'], strike_zone['left']], [strike_zone['bottom'], strike_zone['top']], color='black')
    plt.plot([strike_zone['right'], strike_zone['right']], [strike_zone['bottom'], strike_zone['top']], color='black')

    # White home plate at the bottom
    home_plate_white_x = [-0.75, 0.75, 0.5, -0.5, -0.75]
    home_plate_white_y = [0, 0, -0.15, -0.15, 0]
    plt.fill(home_plate_white_x, home_plate_white_y, 'white', edgecolor='black')

    plt.xlim(-1.5, 1.5)
    plt.ylim(0, 5)
    plt.gca().set_axis_off()
    plt.tight_layout()

    # Encode plot into a base64 image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return "data:image/png;base64,{}".format(data)
