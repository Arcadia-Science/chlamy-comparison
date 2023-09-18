"""
The script reads a CSV file containing metadata and image information,
and iterates over each row to perform a series of image processing
tasks—specifically, cropping, rotating, and thresholding—on masked
images. Each image is first cropped to a 49x49 pixel area, rotated
based on a given angle, and then converted to a binary image.
The major axis orientation of the binary object within the image is
computed, and the image is rotated again based on this orientation.
The processed images are saved to a specified output directory,
which is created if it doesn't already exist. The script employs
various libraries like pandas, PIL, NumPy, OpenCV, and skimage for
 these tasks.
"""

import os
import pandas as pd
from PIL import Image
import numpy as np
import cv2
import math
import numpy.linalg as linalg
from skimage import measure
from skimage.draw import line

def get_major_axis_orientation(binary_image):
    labeled_image = measure.label(binary_image)
    properties = measure.regionprops(labeled_image)
    if not properties:
        return None

    # Assuming the object of interest is the largest by area
    largest_object = max(properties, key=lambda x: x.area)
    return largest_object.orientation  # This is in radians

def crop_and_rotate(image, x, y, angle, output_path):
    # Crop to 49 x 49 pixels
    crop_rectangle_49 = (x - 24, y - 24, x + 25, y + 25)
    cropped_49 = image.crop(crop_rectangle_49)
    cropped_49_np = np.array(cropped_49)
    #save_intermediate_image(cropped_49_np, output_path, "cropped49")

    # Rotate using OpenCV
    M = cv2.getRotationMatrix2D((24, 24), -angle, 1)
    rotated_np = cv2.warpAffine(cropped_49_np, M, (49, 49), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #save_intermediate_image(rotated_np, output_path, "rotated")

    # Convert to 8-bit grayscale for thresholding
    rotated_8bit = cv2.convertScaleAbs(rotated_np, alpha=(255.0/65535.0))
    #save_intermediate_image(rotated_8bit, output_path, "convert")

    # Threshold the 8-bit image (Converting non-zero pixels to 255)
    _, thresholded = cv2.threshold(rotated_8bit, 1, 255, cv2.THRESH_BINARY)
    #save_intermediate_image(thresholded, output_path, "thresholded")

    # Convert thresholded image to binary
    binary_image = thresholded // 255

    # Get major axis orientation in radians
    orientation = get_major_axis_orientation(binary_image)

    # Convert orientation to degrees
    orientation_degrees = np.degrees(orientation)

    # Rotate the image again
    M = cv2.getRotationMatrix2D((24, 24), -orientation_degrees, 1)
    rotated_again_np = cv2.warpAffine(rotated_np, M, (49, 49), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    #save_intermediate_image(rotated_again_np, output_path, "rotated_again")

    # To visualize the major axis, let's draw a line on the image
    #rr, cc = line(24, 24, int(24 + 24 * np.sin(orientation)), int(24 + 24 * np.cos(orientation)))
    #rotated_again_np[rr, cc] = 65535  # Max pixel value for a 16-bit image
    # save_intermediate_image(rotated_again_np, output_path, "major_axis")

    # Convert back to PIL Image for saving
    rotated_again = Image.fromarray(rotated_again_np.astype(np.uint16), 'I;16')

    return rotated_again

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("./experiments/object_image_list_obj_stats.csv")

# Loop through each row in the DataFrame
for index, row in df.iterrows():
    metadata_experiment = row['metadata_experiment']
    metadata_species = row['metadata_species']
    metadata_pool_id = row['metadata_pool_id']
    image_frame = row['image_frame']
    mean_object = row['mean_object']
    well_name = row['well_name']
    Image_name = row['Image']
    center_x = row['Center_X']
    center_y = row['Center_Y']
    angle = row['Angle_with_Y_Axis']

     # Skip rows with NaN values
    if pd.isna(center_x) or pd.isna(center_y) or pd.isna(angle):
        print(f"Skipping row {index} due to NaN values.")
        continue

    # Only process rows where mean_object < 1.1
    if mean_object >= 1.1:
        print(f"Skipping row {index} as mean_object is {mean_object} which is >= 1.1")
        continue

    # Construct the file paths
    mask_path = f"./experiments/{metadata_experiment}/masked/{metadata_species}/{metadata_pool_id}/{Image_name}_mask.tif"
    output_path = f"./experiments/{metadata_experiment}/oriented_major/{metadata_species}/{metadata_pool_id}/{Image_name}_orient.tif"

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Read the masked image
    masked_image = Image.open(mask_path)

    print("Initial image mode:", masked_image.mode)

    # Crop and rotate the image
    cropped_and_rotated = crop_and_rotate(masked_image, center_x, center_y, angle, output_path)

    # Save the cropped and rotated image
    cropped_and_rotated.save(output_path)

    print(f"Saved cropped and rotated image to {output_path}")
