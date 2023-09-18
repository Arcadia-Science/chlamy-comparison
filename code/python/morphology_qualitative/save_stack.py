"""
The script reads a CSV file into a pandas DataFrame and iterates
through each row to load specific images based on the metadata.
It organizes these images into stacks, grouped by a key composed
of experiment and species metadata. Finally, the script saves
these stacks as TIFF files, after ensuring all images in a stack
have the same shape. The image stacks are saved in the
"./experiments" directory.
"""

import os
import pandas as pd
from PIL import Image
import numpy as np
from tifffile import imwrite

# Initialize a dictionary to hold image stacks
image_stacks = {}

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("./experiments/object_image_list_obj_stats.csv")

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    metadata_experiment = row['metadata_experiment']
    metadata_species = row['metadata_species']
    metadata_pool_id = row['metadata_pool_id']
    Image_name = row['Image']

    # Key for image stack
    stack_key = f"{metadata_experiment}_{metadata_species}"

    # Initialize list if key does not exist
    if stack_key not in image_stacks:
        image_stacks[stack_key] = []

    # Construct the file paths
    mask_path = f"./experiments/{metadata_experiment}/oriented_major/{metadata_species}/{metadata_pool_id}/{Image_name}_orient.tif"

    try:
        # Try to read the oriented image
        oriented_image = Image.open(mask_path)
    except FileNotFoundError:
        print(f"File {mask_path} not found. Skipping.")
        continue

    oriented_image_array = np.array(oriented_image)

    # Append to the corresponding list in the dictionary
    image_stacks[stack_key].append(oriented_image_array)

# Save the image stacks as TIFF files
base_directory = "./experiments"
for stack_key, image_list in image_stacks.items():
    stack_file_path = os.path.join(base_directory, f"{stack_key}.tif")

    # Check that all images have the same shape
    unique_shapes = {img.shape for img in image_list}
    if len(unique_shapes) > 1:
        print(f"Skipping {stack_key}: Inconsistent image shapes {unique_shapes}")
        continue

    # Convert list of arrays to single 3D array
    image_stack_array = np.stack(image_list, axis=0)

    imwrite(stack_file_path, image_stack_array, imagej=True)

    print(f"Saved image stack to {stack_file_path}")
