import os
import numpy as np
from skimage.measure import label, regionprops
import tifffile
import csv
import argparse

"""
This script processes a directory of 3D image files to compute the maximum dimensions of the largest segmented region
in each image. The maximum depth, height, and width of these regions are calculated and saved to a specified CSV file.
The script is run from the command line, accepting inputs for the directory of image files, and the path to the output CSV file.
Usage: python script.py --input-dir <path_to_input_directory> --output-csv <path_to_output_csv_file>
"""

# XY_SCALE_FACTOR = 43.0769  # pixels/micron for 1.5x magnifier
XY_SCALE_FACTOR = 64.6154  # pixels/micron for 1.0x magnifier
Z_STEP = 0.1  # micron


def parse_args():
    parser = argparse.ArgumentParser(
        description='Process some images and output the results to a CSV file.')
    parser.add_argument(
        "-i",
        "--input-dir",
        required=True,
        help="Path to the directory containing image files.",
    )
    parser.add_argument(
        "-o",
        "--output-csv",
        required=True,
        help="Path to output CSV file.",
    )
    args = parser.parse_args()
    return args


def get_max_dimensions(segmented_array):
    labeled_array = label(segmented_array)
    largest_region = None
    max_area = 0

    for region in regionprops(labeled_array):
        if region.area > max_area:
            max_area = region.area
            largest_region = region

    if largest_region is None:
        return None, None, None  # No regions found

    minZ, minY, minX, maxZ, maxY, maxX = largest_region.bbox

    depth = (maxZ - minZ) * Z_STEP
    height = (maxY - minY) / XY_SCALE_FACTOR
    width = (maxX - minX) / XY_SCALE_FACTOR

    return depth, height, width


def process_directory(input_directory, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename", "Max Depth (micron)",
                        "Max Height (micron)", "Max Width (micron)"])  # CSV header

        for filename in os.listdir(input_directory):
            if filename.endswith(".tiff"):
                file_path = os.path.join(input_directory, filename)
                segmented_cell = tifffile.imread(file_path)
                depth, height, width = get_max_dimensions(segmented_cell)

                if depth is not None:  # valid region found
                    writer.writerow([filename, depth, height, width])

                print(f"Processed {filename}")


def main(args):
    input_directory = args.input_dir
    output_csv_path = args.output_csv
    process_directory(input_directory, output_csv_path)


if __name__ == "__main__":
    args = parse_args()
    main(args)
