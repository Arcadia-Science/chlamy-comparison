import csv
import cv2
import os
import sys
import numpy as np
from collections import defaultdict

# Summary:
# This script processes images based on data in a CSV file. It rotates, translates, and crops each image based on
# the movement direction of a detected object. The processed images are then saved in new directories, ".../final_transformed_images/...".

def read_csv(file_path):
    """
    Read a CSV file into a dictionary structure.

    Input:
    - file_path (str): The path to the CSV file.

    Output:
    - data (dict): Dictionary containing the organized CSV data.
    """

    # Using defaultdict to automatically initialize lists for new keys
    data = defaultdict(list)

    # Open the CSV file for reading
    with open(file_path, 'r') as infile:

        # Use the DictReader class from the csv module to read rows as dictionaries
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:

            # Group rows by a combination of experiment, species, pool_ID, and seq_number
            key = (row['experiment'], row['species'], row['pool_ID'], row['seq_number'])
            data[key].append(row)
    return data

def rotate_and_translate_images(group_data):
    """
    Process (rotate and translate) a group of images.

    Input:
    - group_data (list): List of rows corresponding to a group of images.
    Output:
    - transformed images
    """
    anchor_row = None
    max_area = -1

    # Find the row with the maximum area where seq_frame is '0'
    for row in group_data:
        if row['seq_frame'] == '0':
            area = float(row.get('area', 0))
            if area > max_area:
                max_area = area
                anchor_row = row

    # If no suitable anchor row is found, print an error message and exit this function
    if anchor_row is None:
        print("No anchor object found.")
        return

    # Try to extract the rotation angle from the anchor row
    try:
        angle_from_csv = float(anchor_row['angle'])
    except ValueError:
        print(f"Could not convert angle to float: {anchor_row['angle']}")
        return

    # Calculate the actual rotation angle based on the extracted value
    rotation_angle = -(-90 - angle_from_csv)
    anchor_centroid = (int(anchor_row['centroid_x']), int(anchor_row['centroid_y']))

    # Define the directory where processed images will be saved
    experiment, species, pool_ID = anchor_row['experiment'], anchor_row['species'], anchor_row['pool_ID']
    final_save_dir = f"./experiments/{experiment}/final_transformed_images/{species}/{pool_ID}"
    os.makedirs(final_save_dir, exist_ok=True)

    # Process each image in the group
    for row in group_data:
        img_path = row['file_path']

        # Read the image in grayscale mode
        img = cv2.imread(img_path, 0)

        # Calculate the rotation matrix and rotate the image
        M_rot = cv2.getRotationMatrix2D(anchor_centroid, rotation_angle, 1)
        rotated_img = cv2.warpAffine(img, M_rot, (img.shape[1], img.shape[0]))

        # Calculate the translation needed to center the anchor object and apply it
        translation = (img.shape[1] // 2 - anchor_centroid[0], img.shape[0] // 2 - anchor_centroid[1])
        M_trans = np.float32([[1, 0, translation[0]], [0, 1, translation[1]]])
        translated_img = cv2.warpAffine(rotated_img, M_trans, (img.shape[1], img.shape[0]))

        # Crop the image to a fixed size of 128x128
        final_size = 128
        start_x = (translated_img.shape[1] - final_size) // 2
        start_y = (translated_img.shape[0] - final_size) // 2
        cropped_img = translated_img[start_y:start_y + final_size, start_x:start_x + final_size]

        # Save the processed image to the final directory
        final_save_path = os.path.join(final_save_dir, os.path.basename(img_path))
        cv2.imwrite(final_save_path, cropped_img)

def main():
    """
    Entry point of the script. Orchestrates reading the CSV, processing the images, and saving the results.
    """

    # Define the path to the input CSV file
    csv_file_path = "experiments/image_data_with_upward_angles.csv"

    # Begin logging all print statements to a file named 'log.txt'
    original_stdout = sys.stdout
    with open('log.txt', 'a') as f:
        sys.stdout = f

        print("Reading CSV data...")
        data = read_csv(csv_file_path)

        print("Starting to process images...")
        for key, group_data in data.items():
            print(f"Processing group: {key}")
            rotate_and_translate_images(group_data)

        print("Processing complete.")

    # After logging is done, reset the standard output to its original state
    sys.stdout = original_stdout

# If this script is run directly, the main function is called
if __name__ == "__main__":
    main()
