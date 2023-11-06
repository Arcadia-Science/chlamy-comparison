import os
import cv2
import csv
import re
import numpy as np
import sys

# Summary:
# The script processes a set of images, identifies objects in them, calculates their centroids, and
# determines the movement direction of the largest object by comparing the centroids between frames.
# The processed data is saved in a CSV file. The primary functions are `find_contours` (for object
# detection) and `main` (for orchestrating the entire process).

def find_contours(image_path):
    """
    Function to find contours of objects in an image.

    Inputs:
    - image_path (str): Path to the image file.

    Outputs:
    - len(object_areas) (int): Number of identified objects.
    - object_areas (list): Areas of the identified objects.
    - centroids (list): Centroids of the identified objects.
    """

    # Read the image
    img = cv2.imread(image_path, 0)

    # Find contours
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter object areas greater than 16
    object_areas = [cv2.contourArea(cnt) for cnt in contours if cv2.contourArea(cnt) > 16]
    centroids = []

    # Calculate centroids for the filtered objects
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 16:
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
            cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
            centroids.append((cX, cY))
    return len(object_areas), object_areas, centroids

def main():
    """
    Entry point of the script. Orchestrates the image processing and data extraction.
    """

    # Output CSV file path
    csv_file_path = "experiments/image_data_with_upward_angles.csv"

    # Create or ensure debug image directory exists
    os.makedirs("experiments/debug_images", exist_ok=True)

    # Start logging to a file
    original_stdout = sys.stdout
    with open('log.txt', 'a') as f:
        sys.stdout = f

        print("Starting to process images...")

        output_rows = []
        processed_rows = set()
        total_rows = 0

        # Walk through the image directory structure
        for root, _, files in os.walk('./experiments/'):
            path_parts = root.split(os.sep)

            # Check directory structure
            if len(path_parts) == 6 and path_parts[3] == 'objects':
                _, _, experiment, _, species, pool_ID = path_parts
                print(f"Processing images in directory: {root}")
                for file_name in files:
                    total_rows += 1
                    file_path = os.path.join(root, file_name)

                    # Extract sequence number and frame from the file name
                    seq_number = re.search(r'_seq(\d+)_', file_name).group(1) if re.search(r'_seq(\d+)_', file_name) else 'NA'
                    seq_frame = re.search(r'_(\d+)\.tif', file_name).group(1) if re.search(r'_(\d+)\.tif', file_name) else 'NA'
                    row_key = (experiment, species, pool_ID, file_name, seq_number, seq_frame)
                    if row_key in processed_rows:
                        print(f"Skipping duplicate row: {row_key}")
                        continue
                    else:
                        processed_rows.add(row_key)

                    # Find contours of objects
                    object_count, object_areas, centroids = find_contours(file_path)

                    # Initialization
                    angles = [None] * object_count

                    # Check for frame 0 as it's compared with frame 3
                    if seq_frame == "0":
                        if len(object_areas) == 0:
                            print(f"No objects found in {file_path}. Skipping...")
                            continue
                        largest_object_index = np.argmax(object_areas)

                        # Compare frame 0 with frame 3
                        for frame_to_compare in ['3']:
                            comparison_file_name = file_name.replace(f"_{seq_frame}.tif", f"_{frame_to_compare}.tif")
                            comparison_file_path = os.path.join(root, comparison_file_name)
                            if not os.path.exists(comparison_file_path):
                                continue
                            _, _, comparison_centroids = find_contours(comparison_file_path)

                            # Ensure centroid counts match
                            if len(centroids) != len(comparison_centroids):
                                continue

                            # Calculate the angle of movement
                            cX1, cY1 = centroids[largest_object_index]
                            cX2, cY2 = comparison_centroids[largest_object_index]
                            dy = cY2 - cY1
                            dx = cX2 - cX1
                            angle = np.arctan2(dy, dx) * 180 / np.pi
                            angles[largest_object_index] = angle

                    # Populate output rows
                    for object_number, (object_area, (cX, cY)) in enumerate(zip(object_areas, centroids), start=1):
                        output_rows.append([experiment, species, pool_ID, file_name, seq_number, seq_frame, object_number, object_area, cX, cY, file_path, angles[object_number - 1] if angles else None])

        # Sort the output rows by the 'file_path' column (index 10)
        output_rows.sort(key=lambda x: x[10])

        # Write the data to CSV
        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['experiment', 'species', 'pool_ID', 'file_name', 'seq_number', 'seq_frame', 'object_number', 'object_area', 'centroid_x', 'centroid_y', 'file_path', 'angle'])
            csv_writer.writerows(output_rows)

        print(f"Filtered out {total_rows - len(processed_rows)} duplicate entries out of {total_rows} total entries.")
        print("Processing complete.")

    # Reset standard output to its original value
    sys.stdout = original_stdout

# Script entry point
if __name__ == "__main__":
    main()
