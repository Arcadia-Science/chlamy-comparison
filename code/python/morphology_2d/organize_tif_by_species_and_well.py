"""
This Python code scans through subdirectories under a `base_directory` labeled as
`./experiments` to find files in "prob_map" directories with names ending with `.tif`.
It logs found files and checks if they follow an expected naming format
(should contain '_seq' and prefixes either 'cr' or 'cs').
The code then organizes these `.tif` files into new directories
based on species ('cr' or 'cs') and pool ID.
"""
# Import necessary modules
import os  # For file and directory operations
import shutil  # For file operations like copy
import logging  # For logging information and warnings

# Initialize the logging system to show info-level messages
logging.basicConfig(level=logging.INFO)

# Define the base directory where experiments are located
base_directory = './experiments'

# Get a list of all experiments; os.listdir gives names of all files and directories in the given directory
# We use os.path.isdir to filter only directories
experiments = [dir for dir in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, dir))]

# Loop over each experiment
for experiment in experiments:
    # Construct the path to the 'prob_maps' subdirectory inside each experiment
    prob_maps_directory = os.path.join(base_directory, experiment, 'prob_maps')
    # Create the new directory path for 'prob_maps_organized'
    prob_maps_organized_directory = os.path.join(base_directory, experiment, 'prob_maps_organized')

    # os.walk goes through all subdirectories and files in a directory
    for dirpath, dirnames, filenames in os.walk(prob_maps_directory):
        # Loop over each file in the directory
        for filename in filenames:
            # Check if the file is a .tif file
            if filename.endswith(".tif"):
                logging.info(f"Found .tif file {filename} in {dirpath}")

                seq_pos = filename.find('_seq')
                if seq_pos == -1:
                    logging.warning(f"Skipping file {filename} in {dirpath} due to missing '_seq'.")
                    continue

                prefix = filename.split('_')[0]
                pool_id = filename[len(prefix)+1:seq_pos]

                if prefix not in ['cr', 'cs']:
                    logging.warning(f"Skipping file {filename} in {dirpath} due to unexpected prefix.")
                    continue

                # Create the new directory under 'prob_maps_organized'
                new_directory = os.path.join(prob_maps_organized_directory, prefix, pool_id)

                # Create the directory if it does not exist
                if not os.path.exists(new_directory):
                    os.makedirs(new_directory)

                # Copy the file to the new directory under 'prob_maps_organized'
                shutil.copy(os.path.join(dirpath, filename), os.path.join(new_directory, filename))
                logging.info(f"Copied {filename} to {new_directory}")

logging.info("Files reorganized successfully!")
