"""The Python script reads in object measurement data from multiple CSV files
stored in a directory structure and combines them into a single DataFrame.
It then reads another CSV file that lists sequences of images, and for each
sequence, it calculates the angle between consecutive vectors formed by the
object's coordinates in three images. Finally, it adds these calculated angles,
along with some other information like coordinates for the "next" image and
angles with the Y-axis, as new columns to the DataFrame and saves it as a
new CSV file."""

import os
import pandas as pd
import numpy as np
import math

# Function to calculate angle between two vectors
def calculate_angle(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude_vec1 = np.linalg.norm(vec1)
    magnitude_vec2 = np.linalg.norm(vec2)

    angle = np.arccos(dot_product / (magnitude_vec1 * magnitude_vec2))
    return math.degrees(angle)


# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Define the base directory
base_directory = "./experiments"

# Load object_measurement data
for root, dirs, files in os.walk(base_directory):
    if '/objects/' in root and 'object_measurements.csv' in files:
        csv_path = os.path.join(root, 'object_measurements.csv')
        data = pd.read_csv(csv_path)

        print(f"Columns in loaded DataFrame from {csv_path}: {data.columns}")
        print("Sample data:", data.head())

        all_data = pd.concat([all_data, data])

# Check if all_data is empty
if all_data.empty:
    print("all_data DataFrame is empty.")

# Read the object_image_list CSV file into a DataFrame
object_image_list_path = "./experiments/object_image_list_frames.csv"  # <-- Correct this path
object_image_list = pd.read_csv(object_image_list_path)

# ... (previous code for imports, function definition, and DataFrame loading)

# Initialize lists to store angles and coordinates
angles = []
coords_next_x = []
coords_next_y = []
angles_with_y_axis = []

# Loop through object_image_list to get the frames
for index, row in object_image_list.iterrows():
    prev_image = row['previous_image']
    current_image = row['Image']
    next_image = row['next_image']

    # Get coordinates for these frames from all_data
    coords_prev = all_data[all_data['Image'] == prev_image][['Center_X', 'Center_Y']].values
    coords_current = all_data[all_data['Image'] == current_image][['Center_X', 'Center_Y']].values
    coords_next = all_data[all_data['Image'] == next_image][['Center_X', 'Center_Y']].values

    # Check if coordinates are available for all frames and that each frame has exactly one object
    if len(coords_prev) == 1 and len(coords_current) == 1 and len(coords_next) == 1:
        # Calculate vectors
        vec1 = coords_current - coords_prev
        vec2 = coords_next - coords_current

        # Calculate angle
        angle = calculate_angle(vec1[0], vec2[0])  # As there's only one row, we can directly use vec1[0] and vec2[0]
        angles.append(angle)

        # Store the coordinates from coords_next
        coords_next_x.append(coords_next[0][0])
        coords_next_y.append(coords_next[0][1])

        # Calculate angle with positive Y-axis
        angle_with_y_axis = math.degrees(math.atan2(vec2[0][0], vec2[0][1]))
        angles_with_y_axis.append(angle_with_y_axis)

    else:
        print(f"Skipping angle calculation for frames: {prev_image}, {current_image}, {next_image} due to multiple objects.")
        angles.append(None)
        coords_next_x.append(None)
        coords_next_y.append(None)
        angles_with_y_axis.append(None)

# Add angles and coordinates as new columns to object_image_list
object_image_list['Swim_Angle'] = angles
object_image_list['coords_next_X'] = coords_next_x
object_image_list['coords_next_Y'] = coords_next_y
object_image_list['Angle_with_Y_Axis'] = angles_with_y_axis

# Save the updated DataFrame as a new CSV file
object_image_list.to_csv("./experiments/object_image_list_angles.csv", index=False)
