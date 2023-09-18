"""
The code is a Python script designed for image segmentation
and analysis of cells in a set of TIFF images.
It uses various scientific libraries like NumPy, SciPy,
scikit-image, and pandas. The `segment_cells` function reads
a "probability map" image, performs thresholding,
and labels individual cell regions, filtering them based on
area constraints defined by min_diameter and max_diameter parameters.
The `save_measurements_to_csv` function takes these labeled regions and
 calculates properties like area, perimeter, and centroids,
 saving them to a CSV file. Metadata from the file paths,
 like experiment details and species, are also extracted and saved.
 The `process_directory` function walks through a given root directory,
 looking for relevant TIFF images and applying the above-mentioned functions.
 The script runs the `process_directory` function for a specified base directory,
 effectively enabling batch processing of cell images for analysis.
"""

# Import required libraries
import numpy as np  # For numerical operations like array manipulations
import os  # For operating system-dependent functionality like reading or writing to the file system
import re  # For regular expression operations
from scipy.ndimage import label, find_objects, sum as ndi_sum  # For image processing
from skimage.io import imread, imsave  # For reading and saving image files
import pandas as pd  # For data manipulation and analysis
from skimage.measure import regionprops  # For measuring properties of labeled image regions

# Function to segment cells in an image
def segment_cells(prob_map_path, threshold=32767.5, min_diameter=3, max_diameter=40):
    # Read the image
    prob_map = imread(prob_map_path)
    # Keep only the first channel (assuming grayscale)
    prob_map = prob_map[:, :, 0]
    # Apply threshold to create a binary image
    binary_map = np.where(prob_map > threshold, 1, 0)
    # Label connected regions in the binary image
    labeled_map, num_features = label(binary_map)

    # Calculate minimum and maximum area based on provided diameters
    min_area = np.pi * (min_diameter / 2) ** 2
    max_area = np.pi * (max_diameter / 2) ** 2

    # Measure properties of labeled regions
    properties = regionprops(labeled_map)
    # Filter regions based on area
    filtered_properties = [prop for prop in properties if min_area <= prop.area <= max_area]

    # Find slices for labeled regions
    slice_objects = find_objects(labeled_map)
    # Remove regions that don't meet area criteria
    for i in range(num_features):
        component = labeled_map[slice_objects[i]]
        area = ndi_sum(1, component, index=i + 1)
        if area < min_area or area > max_area:
            labeled_map[slice_objects[i]] = 0

    # Convert to 8-bit image for saving
    binary_map = binary_map * 255
    return binary_map.astype(np.uint8), filtered_properties

# Function to save properties of segmented cells to a CSV file
def save_measurements_to_csv(prob_map_path, filtered_properties):
    # Prepare path to save CSV
    directory = os.path.dirname(prob_map_path).replace('prob_maps_organized', 'objects')
    csv_save_path = os.path.join(directory, 'object_measurements.csv')

    # Calculate distances for sorting
    distances = [np.sqrt(prop.centroid[0] ** 2 + prop.centroid[1] ** 2) for prop in filtered_properties]
    sorted_indices = np.argsort(distances)

    # Gather measurements into a dictionary
    measurements = {
        'Object_ID': [i + 1 for i in sorted_indices],
        'Image': [os.path.basename(prob_map_path)] * len(filtered_properties),
        'Area': [filtered_properties[i].area for i in sorted_indices],
        'Perimeter': [filtered_properties[i].perimeter for i in sorted_indices],
        'MajorAxisLength': [filtered_properties[i].major_axis_length for i in sorted_indices],
        'MinorAxisLength': [filtered_properties[i].minor_axis_length for i in sorted_indices],
        'Eccentricity': [filtered_properties[i].eccentricity for i in sorted_indices],
        'Center_Y': [filtered_properties[i].centroid[0] for i in sorted_indices],
        'Center_X': [filtered_properties[i].centroid[1] for i in sorted_indices]
    }

    # Extract metadata
    metadata = extract_metadata_from_path(prob_map_path)
    for key, value in metadata.items():
        measurements[key] = [value] * len(filtered_properties)

    # Save as a DataFrame to CSV
    df = pd.DataFrame(measurements)
    if os.path.exists(csv_save_path):
        df.to_csv(csv_save_path, mode='a', header=False, index=False)  # Append if CSV already exists
    else:
        df.to_csv(csv_save_path, mode='w', header=True, index=False)  # Create new CSV
    print(f"Appended measurements to {csv_save_path}")
# Function to extract metadata from a file path
def extract_metadata_from_path(path):
    # Split the path into its components
    components = path.split(os.sep)

    # Extract the 'experiment' metadata from the second part of the path
    metadata_experiment = components[2]

    # Extract the filename from the full path
    filename = os.path.basename(path)

    # Extract the 'species' metadata from the filename by splitting it by underscores
    metadata_species = filename.split('_')[0]

    # Extract the 'pool_id' from the filename
    # Find the starting and ending positions for the substring we want to extract
    start_index = filename.find('pools_') + len('pools_')
    end_index = filename.rfind('_seq')
    # If the start and end positions are valid, extract the substring; otherwise, set to None
    metadata_pool_id = filename[start_index:end_index] if start_index != -1 and end_index != -1 else None

    # Extract the 'frames' from the filename in a similar manner as above
    start_index = filename.find("_f") + 2
    end_index = filename.find("_Prob")
    metadata_frames = filename[start_index:end_index] if start_index != -1 and end_index != -1 else None

    # Extract the 'sequence' metadata
    start_index = filename.find("seq") + 3
    end_index = filename.find("_f")
    metadata_seq = filename[start_index:end_index] if start_index != -1 and end_index != -1 else None

    # Return a dictionary containing all extracted metadata
    return {
        'metadata_experiment': metadata_experiment,
        'metadata_species': metadata_species,
        'metadata_pool_id': metadata_pool_id,
        'metadata_frames': metadata_frames,
        'metadata_sequence': metadata_seq
    }

# Function to process a directory containing image files
def process_directory(root_directory):
    # Loop through each sub-directory and file in the root directory
    for root, dirs, files in os.walk(root_directory):
        # Only process directories that contain 'prob_maps_org' in their name
        if 'prob_maps_org' in root:
            # Loop through each file in the directory
            for filename in files:
                # Only process files with the '.tif' extension
                if filename.endswith('.tif'):
                    # Create the full path to the input file
                    input_path = os.path.join(root, filename)
                    # Create the directory path where the output will be saved, replacing 'prob_maps_organized' with 'objects'
                    output_dir = root.replace('prob_maps_organized', 'objects')
                    # If the output directory doesn't exist, create it
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    # Create the full path to the output file
                    output_path = os.path.join(output_dir, filename)

                    # Run the cell segmentation function on the input file
                    binary_map, properties = segment_cells(input_path)
                    # Save the segmented image
                    imsave(output_path, binary_map)
                    # Save the properties of the segmented cells to a CSV file
                    save_measurements_to_csv(input_path, properties)

# Main function, entry point of the script
if __name__ == "__main__":
    # Starting directory (change this to your specific directory if needed)
    base_directory = "."
    # Call the function to start processing the directory
    process_directory(base_directory)
