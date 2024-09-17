import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.image as mpimg

# Load the background image
img = mpimg.imread('/mnt/data/catcherBG.png')  # Adjust to your image path

def plot_with_background_filled(pitcher, df, side_shift=-1.8, height_shift=-2.15):
    # Filter data for the selected pitcher
    pitcher_data = df[df['pitcher.name'] == pitcher].dropna(subset=['location.plateLocSide', 'location.plateLocHeight'])
    
    # Create the plot with larger dimensions and adjusted limits
    fig, ax = plt.subplots(figsize=(10, 12))

    # Increase the size of the background to cover the whole plot
    ax.imshow(img, extent=[-2.5, 2.5, 0, 7], aspect='auto')  # Adjusted extent to make the background fill the entire plot
    
    # Plot pitch locations
    sns.scatterplot(
        data=pitcher_data,
        x='location.plateLocSide',
        y='location.plateLocHeight',
        hue='pitchTag.taggedPitchType',
        palette={'Fastball': 'red', 'Slider': 'green', 'Splitter': 'purple', 'ChangeUp': '#FFD700'},
        s=100,
        marker='o',
        legend=True,
        ax=ax
    )

    # Shift the release height to be above the strike zone, preserving proportions
    pitcher_data['centered_release_height'] = pitcher_data['release.relHeight'] + height_shift
    pitcher_data['centered_release_side'] = pitcher_data['release.relSide'] + side_shift

    # Add centered release height and release side on the same plot using small dots
    sns.scatterplot(
        data=pitcher_data,
        x='centered_release_side',
        y='centered_release_height',
        hue='pitchTag.taggedPitchType',
        palette={'Fastball': 'red', 'Slider': 'green', 'Splitter': 'purple', 'ChangeUp': '#FFD700'},
        s=20,  # Small dot
        marker='o',
        legend=False,
        ax=ax
    )

    # Plot super flat arcs connecting release point to pitch location
    for i, row in pitcher_data.iterrows():
        release_x, release_y = row['centered_release_side'], row['centered_release_height']
        plate_x, plate_y = row['location.plateLocSide'], row['location.plateLocHeight']

        # Generate t values for interpolation between 0 and 1
        t = np.linspace(0, 1, 100)

        # Define a midpoint control for even flatter arcs, nearly straight
        mid_x = (release_x + plate_x) / 2
        mid_y = release_y + 0.05  # Minimal upward lift for even flatter arcs

        # Use quadratic Bezier-like interpolation to create a smooth, super flat arc
        arc_x = (1 - t)**2 * release_x + 2 * (1 - t) * t * mid_x + t**2 * plate_x
        arc_y = (1 - t)**2 * release_y + 2 * (1 - t) * t * mid_y + t**2 * plate_y

        # Plot the arc, matching the line color to the pitch type
        pitch_color = {'Fastball': 'red', 'Slider': 'green', 'Splitter': 'purple', 'ChangeUp': '#FFD700'}
        ax.plot(arc_x, arc_y, color=pitch_color[row['pitchTag.taggedPitchType']], alpha=0.8)

    # Define strike zone with preserved proportions
    strike_zone = {'top': 3.5, 'bottom': 1.5, 'left': -0.71, 'right': 0.71}
    ax.plot([strike_zone['left'], strike_zone['right']], [strike_zone['top'], strike_zone['top']], color='black')
    ax.plot([strike_zone['left'], strike_zone['right']], [strike_zone['bottom'], strike_zone['bottom']], color='black')
    ax.plot([strike_zone['left'], strike_zone['left']], [strike_zone['bottom'], strike_zone['top']], color='black')
    ax.plot([strike_zone['right'], strike_zone['right']], [strike_zone['bottom'], strike_zone['top']], color='black')

    # White home plate at the bottom
    home_plate_white_x = [-0.75, 0.75, 0.5, -0.5, -0.75]
    home_plate_white_y = [0, 0, -0.15, -0.15, 0]
    ax.fill(home_plate_white_x, home_plate_white_y, 'white', edgecolor='black')

    # Adjusting x and y limits to center everything and fit the plot while preserving the strike zone proportions
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(0, 7)
    ax.set_aspect('auto', adjustable='box')  # Allow more flexible aspect ratio to fill the space
    ax.set_axis_off()

    plt.tight_layout()
    plt.show()

# Call the function to display the plot with the fully enlarged background to fill the plot
plot_with_background_filled("Estridge, Gaines", df_combined_with_flight)
