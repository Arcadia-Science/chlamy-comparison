import os
import cv2
import csv
import re
import math
import sys
from itertools import groupby
from operator import itemgetter

# Summary:
# This script processes images, identifies contours, and computes both angular and linear displacements
# between contours in consecutive frames. The results are saved to a CSV file.

def find_closest_contour_to_point(image_path, reference_point=None):
    """
    Identify the contour in the image that's closest to the reference point.

    Inputs:
    - image_path (str): Path to the image.
    - reference_point (tuple, optional): Coordinates (x, y) for reference. If not given, the center of the image is used.

    Outputs:
    - tuple: Centroid of the closest contour, or None if no contours are found.
    """
    # Read the image from the provided path.
    # The second argument '0' indicates that the image should be loaded in grayscale mode.
    img = cv2.imread(image_path, 0)

    # Find the contours in the image.
    # cv2.RETR_EXTERNAL retrieves only the extreme outer contours.
    # cv2.CHAIN_APPROX_SIMPLE compresses horizontal, diagonal, and vertical segments and leaves only their end points.
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours are found in the image, return None.
    if len(contours) == 0:
        return None

    # If no reference point is provided, use the center of the image as the reference point.
    if reference_point is None:
        reference_point = (img.shape[1] // 2, img.shape[0] // 2)

    def distance_from_ref(centroid):
        """Calculate the squared distance between a centroid and the reference point."""

        # If centroid or reference point is None, return a very large distance (infinity).
        if centroid is None or reference_point is None:
            return float('inf')
        return (centroid[0] - reference_point[0])**2 + (centroid[1] - reference_point[1])**2

    def compute_centroid(cnt):
        """Calculate the centroid of a contour."""
        # Compute moments of the contour which can be used to find its centroid.
        M = cv2.moments(cnt)

        # If the area (M["m00"]) is zero, return None.
        if M["m00"] == 0:
            return None

        # Otherwise, compute the x and y coordinates of the centroid.
        return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # Find the contour that is closest to the reference point.
    # This is done by computing the distance of each contour's centroid to the reference point and picking the smallest.
    closest_contour = min(contours, key=lambda cnt: distance_from_ref(compute_centroid(cnt)) if compute_centroid(cnt) is not None else float('inf'))

    # Return the centroid of the closest contour.
    return compute_centroid(closest_contour)

def compute_angle_between_three_frames(previous_frame_path, current_frame_path, next_frame_path):
    """
    Compute the angular and linear displacements between three frames based on object movement.

    Inputs:
    - previous_frame_path (str): Path to the previous frame.
    - current_frame_path (str): Path to the current frame.
    - next_frame_path (str): Path to the next frame.

    Outputs:
    - tuple: Angular displacement in degrees and linear displacement.
             Returns (None, None) if either can't be computed.
    """
    centroid_prev = find_closest_contour_to_point(previous_frame_path)
    centroid_curr = find_closest_contour_to_point(current_frame_path, centroid_prev)
    centroid_next = find_closest_contour_to_point(next_frame_path, centroid_curr)

    if not all([centroid_prev, centroid_curr, centroid_next]):
        print("Missing centroids for one of the frames.")
        return None, None

    # Compute vectors between centroids
    AB = (centroid_curr[0] - centroid_prev[0], centroid_curr[1] - centroid_prev[1])
    BC = (centroid_next[0] - centroid_curr[0], centroid_next[1] - centroid_curr[1])

    # Calculate magnitudes of these vectors
    magnitude_AB = math.sqrt(AB[0]**2 + AB[1]**2)
    magnitude_BC = math.sqrt(BC[0]**2 + BC[1]**2)

    # If vectors are zero, return None
    if magnitude_AB == 0 or magnitude_BC == 0:
        print("Zero vector magnitude detected.")
        return None, None

    # Compute the dot product of vectors
    dot_product = AB[0] * BC[0] + AB[1] * BC[1]
    cos_theta = dot_product / (magnitude_AB * magnitude_BC)
    cos_theta = max(-1.0, min(1.0, cos_theta))

    angle = math.degrees(math.acos(cos_theta))
    print(f"Computed angle: {angle}")
    return angle

def compute_linear_displacement_between_two_frames(current_frame_path, next_frame_path):
    """
    Compute the linear displacement between two frames based on object movement.
    """
    centroid_curr = find_closest_contour_to_point(current_frame_path)
    centroid_next = find_closest_contour_to_point(next_frame_path, centroid_curr)

    if not all([centroid_curr, centroid_next]):
        return None

    # Compute the linear displacement between current and next frames
    linear_displacement = math.sqrt((centroid_next[0] - centroid_curr[0])**2 + (centroid_next[1] - centroid_curr[1])**2)

    return linear_displacement

def main():
    """
    Entry point of the script.
    """
    csv_file_path = "experiments/centroids_displacements.csv"

    # Redirect all print statements to a log file for tracking
    original_stdout = sys.stdout
    with open('log.txt', 'a') as f:
        sys.stdout = f
        print("Starting to process images...")

        with open(csv_file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Add a new column for 'linear_displacement'
            csv_writer.writerow(['experiment', 'species', 'pool_ID', 'seq_number', 'file_name', 'seq_frame', 'centroid_x', 'centroid_y', 'file_path', 'angular_displacement', 'linear_displacement'])

            # Walk through all directories and files under the 'experiments' directory
            for root, _, files in os.walk('./experiments/'):
                # Split the directory path into its individual parts
                path_parts = root.split(os.sep)

                # Check if the current directory is the 'final_transformed_images' sub-directory and has the expected structure
                if len(path_parts) == 6 and path_parts[3] == 'final_transformed_images':
                    _, _, experiment, _, species, pool_ID = path_parts
                    print(f"Processing images in directory: {root}")

                    # List to store data extracted from filenames
                    files_data = []
                    for file_name in files:
                        # Extract sequence number and frame number from the file name using regular expressions
                        seq_number = re.search(r'_seq(\d+)_', file_name).group(1) or 'NA'
                        seq_frame = re.search(r'_(\d+)\.tif', file_name).group(1) or 'NA'
                        file_path = os.path.join(root, file_name)
                        files_data.append((experiment, species, pool_ID, seq_number, file_name, seq_frame, file_path))

                    # Sort the data based on sequence number and frame number for consistent processing
                    files_data.sort(key=itemgetter(3, 5))

                    for key, group in groupby(files_data, key=itemgetter(0, 1, 2, 3)):
                        group_list = list(group)

                        for index, data in enumerate(group_list):
                            experiment, species, pool_ID, seq_number, file_name, seq_frame, file_path = data
                            print(f"  Processing file: {file_name}")

                            angle, linear_disp = None, None

                            # Compute angular displacement if it's the third frame or later
                            if index >= 2:
                                previous_frame = group_list[index-2][-1]
                                current_frame = group_list[index-1][-1]
                                next_frame = file_path
                                angle = compute_angle_between_three_frames(previous_frame, current_frame, next_frame)

                            # Only compute linear displacement if it's not the first or second frame
                            if 1 < index < len(group_list):
                                linear_disp = compute_linear_displacement_between_two_frames(group_list[index-1][-1], file_path)

                            # Find the centroid of the contour in the current image
                            centroid = find_closest_contour_to_point(file_path)

                            # If a centroid is found, write the data to the CSV file
                            if centroid:
                                csv_writer.writerow([experiment, species, pool_ID, seq_number, file_name, seq_frame, centroid[0], centroid[1], file_path, angle, linear_disp])

            print("Processing complete.")

        # Return standard output back to its original value
        sys.stdout = original_stdout

if __name__ == "__main__":
    main()
