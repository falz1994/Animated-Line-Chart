import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Original table
years_original = np.arange(2000, 2011)
y_values_original = np.random.uniform(-10, 10, size=len(years_original))
original_table = pd.DataFrame({'Year': years_original, 'Valor': y_values_original})
print(original_table)

# Create a new table with interpolated values
years_interpolated = np.arange(2000, 2010.01, 0.05)  # Increment by 0.05
interpolated_table = pd.DataFrame({'Year': years_interpolated})

# Perform linear interpolation for the 'Valor' column
interpolated_table['Valor'] = np.interp(
    interpolated_table['Year'],
    original_table['Year'],
    original_table['Valor']
)
print(interpolated_table)
# Create a figure and axis for the line chart
fig, ax = plt.subplots()
ax.set_xlabel('Year')
ax.set_ylabel('Valor')
ax.set_title('Animated Time Series Line Chart')

# Set specific colors for lines and points
line_color = 'blue'
point_color = 'red'

# Highlight the "Middle East War" context (gray zone) with a label
ax.axvspan(2002, 2004, color='gray', alpha=0.3, label='Middle East War')
ax.text(2003, interpolated_table['Valor'].max(), 'Middle East War', rotation=0, ha='center', va='center', color='white', fontweight='bold')

# Add a text label for the (x, y) point
point_label = ax.text(0.5, 1.1, '', transform=ax.transAxes, ha='center', va='bottom')

# Animation function
def update(frame):
    current_year = interpolated_table['Year'].iloc[frame]

    # Plot the line in blue
    x_values = np.linspace(interpolated_table['Year'].iloc[0], current_year, num=500)
    
    # Interpolate y values using cumulative sum of data
    y_interp = np.interp(x_values, interpolated_table['Year'].iloc[:frame+1], interpolated_table['Valor'].iloc[:frame+1])

    line, = ax.plot(x_values, y_interp, label='Interpolated Data', color=line_color)

  
    # Plot individual points in red at every 10th frame
    if frame % 20 == 0:
        current_point = (current_year, y_interp[-1])
        ax.plot(current_point[0], current_point[1], marker='o', markersize=5, color=point_color)

        # Update the (x, y) point label
        point_label.set_text(f'Point: ({current_point[0]:.2f}, {current_point[1]:.3f})')
        print(f'Frame: {frame}, Point: ({current_year:.2f}, {y_interp[-1]:.3f})')


    ax.set_xticks(np.arange(int(interpolated_table['Year'].iloc[0]), int(current_year) + 1))
    ax.relim()
    ax.autoscale_view()

    return line, point_label

# Animation frames
frames = len(interpolated_table)
animation = FuncAnimation(fig, update, frames=frames, interval=100, blit=False)

# Show the plot
plt.show()
