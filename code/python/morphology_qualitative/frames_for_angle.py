"""
The code reads an existing CSV file into a Pandas DataFrame,
defines a function `generate_image_names` to calculate the previous
and next image names based on the frame number found in the original image name,
applies this function to populate new columns for 'previous_image'
and 'next_image', and then saves the modified DataFrame back to a new CSV file.
"""

import pandas as pd
import re

# Load the existing CSV file into a DataFrame
df = pd.read_csv("./experiments/object_image_list.csv")

# Function to create previous and next image names
def generate_image_names(image_name):
    # Use regular expression to find the frame number (the number between the last "_" and ".tif")
    match = re.search(r'_(\d+)\.tif$', image_name)
    if match:
        frame_number_str = match.group(1)
        frame_number = int(frame_number_str)

        # Skip processing if the frame number is 0
        if frame_number == 0:
            return None, None

        # Generate the previous and next frame numbers
        prev_frame_number = frame_number - 1
        next_frame_number = frame_number + 1

        # Format them with the same number of digits as the original frame_number
        prev_frame_number_str = str(prev_frame_number).zfill(len(frame_number_str))
        next_frame_number_str = str(next_frame_number).zfill(len(frame_number_str))

        # Replace the old frame number with the new ones in the image name
        prev_image_name = image_name.replace(f"_{frame_number_str}.tif", f"_{prev_frame_number_str}.tif")
        next_image_name = image_name.replace(f"_{frame_number_str}.tif", f"_{next_frame_number_str}.tif")

        return prev_image_name, next_image_name
    else:
        return None, None

# Apply the function to each row in the DataFrame to populate the new columns
df['previous_image'], df['next_image'] = zip(*df['Image'].apply(generate_image_names))

# Save the modified DataFrame back to the same CSV file (or to a new file, if you prefer)
df.to_csv("./experiments/object_image_list_frames.csv", index=False)
