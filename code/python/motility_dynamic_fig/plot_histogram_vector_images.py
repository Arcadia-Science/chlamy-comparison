"""
Summary:
    This script performs multiple visualization tasks on data read from a CSV file named 'merged_data.csv'.
    First, it creates and saves vector plots for different groups in the data, with each plot displaying a
    vector and an associated average angular velocity. Then, it generates a histogram displaying the frequency
    of bins by species for seq_frame=0. The vector plots are saved as grayscale 8-bit TIFF images in specific
    directories, and the histogram is saved as a PNG.

Inputs:
    - experiments/merged_data.csv: Input CSV file containing the data to be visualized.

Outputs:
    - Vector plots saved as grayscale 8-bit TIFF images.
    - A histogram PNG image named 'histogram_for_fig.png'.

Logging:
    - All operations and exceptions will be logged into 'script_log.txt'.

Entry Point:
    The script starts its execution from the `if __name__ == '__main__':` block, which calls the `main` function.
"""

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from itertools import groupby
from operator import itemgetter

# Logging setup
import logging
logging.basicConfig(filename='script_log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log(message):
    """Utility function to log messages to both the log file and stdout."""
    logging.info(message)
    print(message)

def plot_histogram_of_bins(data):
    """Plot a histogram displaying the frequency of bins by species for seq_frame=0."""
    log("Entering plot_histogram_of_bins...")
    species_list = list(set(row['species'] for row in data))
    colors = ['magenta', 'cyan']  # Modify colors if more species are present
    unique_bins = sorted(list(set(row['bin'] for row in data if row['seq_frame'] == 0)))

    # Set up the bins for the histogram
    hist_bins = [x - 0.5 for x in unique_bins] + [unique_bins[-1] + 0.5]

    plt.figure(figsize=(10, 6))
    ax = plt.gca()  # Get the current axes instance

    # Plot histogram for each species
    for species, color in zip(species_list, colors):
        bins_data_for_species = [row['bin'] for row in data if row['species'] == species and row['seq_frame'] == 0]
        plt.hist(bins_data_for_species, bins=hist_bins, edgecolor="k", alpha=0.7, label=species, color=color)

    plt.xticks(unique_bins)  # Set x-ticks to be the unique bin values
    plt.title("Frequency of Bins by Species for seq_frame = 0", color='white')
    plt.xlabel("Bin", color='white')
    plt.ylabel("Frequency", color='white')
    plt.legend()
    plt.tick_params(axis='y', which='both', length=10, color='white')
    plt.tick_params(axis='x', which='both', length=0, color='white')
    plt.tight_layout()

    # Set the color of tick labels to white
    plt.xticks(color='white')
    plt.yticks(color='white')

    # Set the background color of the axes and the figure to transparent
    plt.gca().set_facecolor('none')
    plt.gcf().set_facecolor('none')

    # Set the color of the spines to white
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    plt.savefig("histogram_for_fig.png", transparent=True)
    plt.close()
    log("Exiting plot_histogram_of_bins...")

def plot_and_save_vectors(data, bin_categories, avg_velocities):
    """Generate and save vector plots for different groups in the data."""
    log("Entering plot_and_save_vectors...")
    for key, group in groupby(data, key=lambda x: (x['experiment'], x['species'], x['pool_ID'], x['seq_number'])):
        group_list = list(group)

        # Use the bin category from bin_categories dictionary
        bin_category = bin_categories.get(key)
        if bin_category is None:
            print(f"Warning: Missing bin category for key {key}. Using 'unknown'.")
            bin_category = 'unknown'

        # Extract x and y coordinates
        x_coords = [int(item['centroid_x']) for item in group_list]
        y_coords = [int(item['centroid_y']) for item in group_list]

        # Get the size of the image from the first entry
        img_path = group_list[0]['file_path']
        img = plt.imread(img_path)
        height, width = img.shape

        for i in range(len(x_coords) - 1):
            plt.figure(figsize=(10,10))
            plt.quiver(x_coords[i], y_coords[i],
                       x_coords[i+1] - x_coords[i],
                       y_coords[i+1] - y_coords[i],
                       angles='xy', scale_units='xy', scale=1, color='k',
                       headlength=0, headwidth=0, headaxislength=0)
            plt.xlim(0, width)
            plt.ylim(height, 0)

            # After plotting the vector and before saving, add the average angular velocity to the image:
            avg_velocity = avg_velocities.get(key, 0)  # get the average velocity for this group
            plt.text(10, 10, f"Avg Angular Velocity: {avg_velocity:.2f}", color='red', backgroundcolor='white')

            # Convert the plot to grayscale 8-bit TIFF image and save
            plt.axis('off')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.margins(0,0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

            experiment, species, pool_ID, seq_number = key

            # Use the bin category from bin_categories dictionary
            bin_category = bin_categories.get(key, 'unknown')
            save_dir = f"./experiments/vectors_sampled_binned/bin_{bin_category}/{species}/"
            os.makedirs(save_dir, exist_ok=True)

            # Include pool_ID, seq_number, and seq_frame in the filename
            seq_frame = group_list[i]['seq_frame']
            save_path = os.path.join(save_dir, f"vector_{pool_ID}_{seq_number}_{seq_frame}.tif")

            # Convert plot to a numpy array
            plt.draw()
            plot_as_np_array = np.frombuffer(plt.gcf().canvas.buffer_rgba(), dtype=np.uint8)
            plot_as_np_array = plot_as_np_array.reshape(plt.gcf().canvas.get_width_height()[::-1] + (4,))

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(plot_as_np_array, cv2.COLOR_RGBA2GRAY)

            # Save as 8-bit TIFF
            cv2.imwrite(save_path, gray_image)

            plt.close()
    log("Exiting plot_and_save_vectors...")

def main():
    """Main function to orchestrate the visualization tasks."""
    log("Entering main...")
    try:
        # Read the CSV
        log("Reading CSV...")
        data = pd.read_csv('experiments/merged_data.csv').to_dict('records')
        log("CSV read successfully!")

        # Create bin_categories and avg_velocities dictionaries
        bin_categories = {(row['experiment'], row['species'], row['pool_ID'], row['seq_number']): row['bin'] for row in data}
        avg_velocities = {(row['experiment'], row['species'], row['pool_ID'], row['seq_number']): row['avg_displacement'] for row in data}

        # Plot and save the vectors
        plot_and_save_vectors(data, bin_categories, avg_velocities)

        # Plot histogram of bins
        plot_histogram_of_bins(data)
    except Exception as e:
        log(f"Error encountered: {e}")
    log("Exiting main...")

# Entry point of the script
if __name__ == '__main__':
    main()
