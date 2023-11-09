import pandas as pd
import os
from PIL import Image
import numpy as np

# Function to align the major axis of an image
def align_major_axis(image_path, orientation_angle):
    # Open the image file
    with Image.open(image_path) as img:
        # Rotate the image to align the major axis upright
        rotated_img = img.rotate(-np.degrees(orientation_angle), expand=True)
        # Save the rotated image with "_aligned" appended to the original filename
        rotated_img.save(image_path[:-4] + "_aligned.tif")

# Replace the directory paths with the paths where your CSV and TIFF files are stored
csv_directory = 'path_to_csv_files_directory'  # e.g., '/path/to/csv/directory'
tif_directory = 'path_to_tif_files_directory'  # e.g., '/path/to/tif/directory'

# Iterate over all CSV files in the given directory
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith(".csv"):
        csv_path = os.path.join(csv_directory, csv_file)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_path)

        # Remove the file extension to create a base filename
        base_filename = os.path.splitext(csv_file)[0]

        # Iterate over each row in the DataFrame
        for _, row in df.iterrows():
            # Extract the orientation and handle NaN values
            orientation = row['Mean_IdentifyPrimaryObjects_AreaShape_Orientation']  # Update with the actual column name
            if np.isnan(orientation):
                print(f"Skipped {base_filename}_cell_{int(row['ImageNumber'])}.tif due to NaN orientation.")
                continue

            # Construct the image filename and path
            image_filename = f"{base_filename}_cell_{int(row['ImageNumber'])}.tif"
            image_path = os.path.join(tif_directory, image_filename)

            # Check if the image file exists and align it if it does
            if os.path.exists(image_path):
                align_major_axis(image_path, orientation)
            else:
                # Log an error if the image file does not exist
                print(f"Image not found: {image_path}")

# Indicate that the process is complete
print("Process completed!")
