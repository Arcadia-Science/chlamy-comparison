import os
import numpy as np
from skimage.measure import label, regionprops
import tifffile
import csv

# XY_SCALE_FACTOR = 43.0769  # pixels/micron for 1.5x magnifier
XY_SCALE_FACTOR = 64.6154  # pixels/micron for 1.0x magnifier
Z_STEP = 0.1  # micron


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


if __name__ == "__main__":
    input_directory = "/Volumes/Microscopy/Theia/Matus/Chlamy_decon/aics/Cs/Cs_chloro_aics"
    output_csv_path = "output_dimensionsCs_chloro.csv"
    process_directory(input_directory, output_csv_path)
