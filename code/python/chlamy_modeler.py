import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

# Given dimensions in um
mean_length = 10 # set your measured length mean
mean_width = 7  # set your measured width mean

# Given standard deviations in um
std_dev_length = 2 # set your measured length std. dev.
std_dev_width = 1 # set your measured width std. dev.

# Given eccentricity and its standard deviation
mean_eccentricity = 0.5 # set your measured eccentricity mean
std_dev_eccentricity = 0.03 # set your measured eccentricity std. dev.

# Create figure and axes
fig, ax = plt.subplots(1)

# Create an Ellipse patch for mean cell dimensions
ellipse = Ellipse((0, 0), width=mean_length, height=mean_width, edgecolor='r', facecolor='none')

# Create Ellipse patches for +1 and -1 standard deviations
ellipse_std_dev_plus = Ellipse((0, 0), width=mean_length + std_dev_length, height=mean_width + std_dev_width, edgecolor='b', facecolor='none')
ellipse_std_dev_minus = Ellipse((0, 0), width=max(mean_length - std_dev_length, 0), height=max(mean_width - std_dev_width, 0), edgecolor='b', facecolor='none')

# Add the patches to the Axes
ax.add_patch(ellipse)
ax.add_patch(ellipse_std_dev_plus)
ax.add_patch(ellipse_std_dev_minus)

# Showing the eccentricity
print("Eccentricity: {:.4f} ± {:.5f}".format(mean_eccentricity, std_dev_eccentricity))

# Setting the limits of the plot
ax.set_xlim([-10, 10]) # set the x-axis range to -10 to 10
ax.set_ylim([-10, 10]) # set the y-axis range to -10 to 10
ax.set_aspect('equal', 'box')

# Save the figure as an SVG file so it can be edited in illustrator
plt.savefig("filename.svg", format='svg') #replace filename with the sample descriptor

# Showing the plot
plt.show()

