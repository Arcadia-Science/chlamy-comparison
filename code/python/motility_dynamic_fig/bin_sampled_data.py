"""
Summary:
    This script reads data from an input CSV file, bins the 'avg_displacement' values into 18 bins,
    and assigns each row a bin number based on its 'avg_displacement' value. The binned data is
    then written to an output CSV file.

Inputs:
    input_path: Path to the input CSV file.
    output_path: Path to the output CSV file where binned data will be saved.

Outputs:
    A new CSV file with data that includes an additional 'bin' column to indicate the bin number
    corresponding to each 'avg_displacement' value.

Entry Point:
    The script starts its execution from the `if __name__ == "__main__":` block.
"""

import csv
import numpy as np

def read_csv(file_path):
    """
    Reads data from a CSV file and returns it as a list of dictionaries.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[Dict[str, Any]]: List of rows from the CSV where each row is represented as a dictionary.
    """
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def determine_bin_category(value, bins):
    """
    Determine the bin category for the given value based on the specified bin edges.

    Args:
        value (float): The value to be binned.
        bins (List[float]): List of bin edges.

    Returns:
        int: Bin category number for the given value.
    """
    if value <= bins[0]:
        return 1
    for i in range(len(bins) - 1):
        if bins[i] <= value < bins[i + 1]:
            return i + 1
    return len(bins) - 1

# Entry point of the script
if __name__ == "__main__":
    # Define input and output paths
    input_path = "experiments/sampled_unbinned_data.csv"
    output_path = "experiments/sampled_binned_data.csv"

    # Read data from input CSV
    data = read_csv(input_path)

    # Extract all 'avg_displacement' values and convert them to float
    avg_displacements = [float(row['avg_displacement']) for row in data]

    # Determine the bin edges for 18 bins
    bin_edges = np.linspace(min(avg_displacements), max(avg_displacements), 19)

    # Assign each row a bin number based on its 'avg_displacement' value
    for row in data:
        value = float(row['avg_displacement'])
        bin_number = determine_bin_category(value, bin_edges)
        row['bin'] = bin_number

    # Write the binned data to a new CSV file
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    # Print the path to the saved binned data
    print(f"Binned data saved to {output_path}")
