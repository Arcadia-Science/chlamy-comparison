"""
The script is designed to process a collection of TIF image stacks,
focusing on identifying and isolating in-focus frames within each stack.
It navigates through a specified root directory
and its subdirectories looking for TIF files,
then applies a focus measure algorithm to each frame in these stacks
to determine which are in focus.
Finally, it saves the in-focus frames
and their adjacent frames as new TIF files,
organized by experiment and species, in an output directory.
"""


# Import required libraries
import os
import numpy as np
import cv2
import tifffile
from skimage import io
from itertools import groupby, count

# Compute focus measure using the variance of Laplacian
def compute_focus_measure(frame):
    return cv2.Laplacian(frame, cv2.CV_64F).var()

# Find sequences of consecutive numbers in a list
def find_consecutive_sequences(nums):
    consec_sequences = []  # List to hold sequences
    current_sequence = [nums[0]]  # Start with the first number
    for i in range(1, len(nums)):
        if nums[i] == current_sequence[-1] + 1:
            current_sequence.append(nums[i])  # Append to current sequence
        else:
            consec_sequences.append(current_sequence)  # Save the previous sequence
            current_sequence = [nums[i]]  # Start a new sequence
    consec_sequences.append(current_sequence)  # Add the final sequence
    return consec_sequences

# Process a TIF stack and find in-focus frames
def process_tif_stack(stack_path, percentile, exclude_start=4, exclude_end=4):
    original_stack = io.imread(stack_path)

    # Exclude frames from the start and end
    if exclude_start + exclude_end >= len(original_stack):
        raise ValueError("Exclusion indices exceed available frame count.")
    stack = original_stack[exclude_start:-exclude_end]

    # Compute focus measures and find the threshold
    focus_measures = np.array([compute_focus_measure(frame) for frame in stack])
    threshold = np.percentile(focus_measures, percentile)
    in_focus_indices = np.where(focus_measures > threshold)[0]

    # Adjust the in-focus indices
    in_focus_indices += exclude_start

    # Create a list of all relevant frames
    all_relevant_frames = list(in_focus_indices)
    for idx in in_focus_indices:
        adjacent_frames = set(range(max(0, idx - 3), min(len(original_stack), idx + 4)))
        all_relevant_frames.extend(adjacent_frames)

    # Remove duplicates and sort the list
    all_relevant_frames = sorted(list(set(all_relevant_frames)))
    return original_stack, all_relevant_frames

# Process directories and TIF files within them
def process_directory(root_directory, percentile):
    # Check if root directory exists
    if not os.path.exists(root_directory):
        raise FileNotFoundError(f"Directory '{root_directory}' not found.")

    # Validate percentile value
    if percentile < 0 or percentile > 100:
        raise ValueError("Percentile must be between 0 and 100.")

    # Traverse directories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        if "pools_sample" in dirpath:
            for filename in filenames:
                if filename.endswith('.tif'):
                    input_path = os.path.join(dirpath, filename)

                    # Parse directory path to get experiment, species, and base name
                    parts = dirpath.split(os.sep)
                    experiment = parts[-3]
                    species = parts[-1]
                    base_name = os.path.splitext(filename)[0]

                    # Create output directory if it doesn't exist
                    output_root = os.path.join(root_directory, experiment, "focus_sample", species, base_name)
                    if not os.path.exists(output_root):
                        os.makedirs(output_root)

                    try:
                        # Process TIF files and save output
                        stack, all_relevant_frames = process_tif_stack(input_path, percentile)
                        sequences = find_consecutive_sequences(all_relevant_frames)

                        for seq_num, sequence in enumerate(sequences, start=1):
                            output_path = os.path.join(output_root, f"{base_name}_seq{seq_num}_f{sequence[0]}to{sequence[-1]}.tif")
                            tifffile.imwrite(output_path, stack[sequence])
                    except Exception as e:
                        print(f"An error occurred while processing {filename}: {e}")

# Entry point
if __name__ == "__main__":
    root_dir = "./experiments/"  # Starting directory
    percentiles = [95]  # List of percentiles to use
    process_directory(root_dir, percentiles[0])  # Start processing
    print("Processing complete.")  # Indicate completion
