"""
The script reads metadata and image information from a CSV file using
the pandas library and iterates over each row to perform image masking.
For each row, it constructs file paths for mask and image files,
reads them using the PIL library, and applies a mask where the mask
value is 255. The masked images are then saved to a specified output
directory, which is created if it doesn't already exist. The script
also includes utility functions to extract specific text substrings
from the image names for further processing.
"""

import os
import pandas as pd
from PIL import Image
import numpy as np

def get_text_before_probab(input_string):
    index = input_string.find("_Probab")
    if index != -1:
        return input_string[:index]
    else:
        return "String does not contain '_Probab'"

def get_text_before_seq(input_string):
    index = input_string.find("_seq")
    if index != -1:
        return input_string[:index]
    else:
        return "String does not contain '_seq'"


# Read the CSV file into a pandas DataFrame
df = pd.read_csv("./experiments/object_image_list_angles.csv")

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    metadata_experiment = row['metadata_experiment']
    metadata_species = row['metadata_species']
    image_frame = row['seq_frame']
    well_name = row['well_name']
    Image_name = row['Image']
    image_stack = get_text_before_probab(Image_name)
    metadata_pool_id = row['metadata_pool_id']
    focus_pool_id = get_text_before_seq(Image_name)

    # Construct the file paths
    mask_path = f"./experiments/{metadata_experiment}/max_area/{metadata_species}/{metadata_pool_id}/{Image_name}"
    image_path = f"./experiments/{metadata_experiment}/focus/{metadata_species}/{focus_pool_id}/{image_stack}.tif"
    output_path = f"./experiments/{metadata_experiment}/masked/{metadata_species}/{metadata_pool_id}/{Image_name}_mask.tif"

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Read the mask and image
    mask = Image.open(mask_path).convert("L")
    image_stack = Image.open(image_path)
    print("Processing image " + image_path)
    print("Processing frame " + str(image_frame))
    image_stack.seek(image_frame)  # Navigate to the frame we care about

    # Perform masking
    mask_array = np.array(mask)
    image_array = np.array(image_stack)

    # Here 255 is the value representing the mask. Change accordingly if your mask uses a different value.
    masked_image_array = np.where(mask_array == 255, image_array, 0)

    # Save the masked image
    masked_image = Image.fromarray(masked_image_array.astype("uint16"))
    masked_image.save(output_path)

    print(f"Saved masked image to {output_path}")
