import csv
from itertools import groupby
import numpy as np

# SUMMARY:
# This script processes data from a CSV file containing angular displacements from experiments.
# The main steps are:
# 1. Read data from the CSV file.
# 2. Filter the data to include only specific allowed experiments.
# 3. Calculate the mean absolute angular displacement for each unique combination of parameters.
# 4. Write the processed data with average displacements to a new CSV file.

def read_csv(file_path):
    """
    Read data from a CSV file and return it as a list of dictionaries.

    Parameters:
        - file_path (str): Path to the CSV file.

    Returns:
        - list: A list of dictionaries where each dictionary represents a row in the CSV.
    """
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def filter_data_by_experiment(data, allowed_experiments):
    """
    Filter the data to only include rows from the allowed experiments.

    Parameters:
        - data (list): List of dictionaries containing the data.
        - allowed_experiments (list): List of experiment names to be included.

    Returns:
        - list: Filtered data.
    """
    return [row for row in data if row['experiment'] in allowed_experiments]

def calculate_mean_displacement(data):
    """
    Calculate the mean absolute angular displacement for each unique combination of parameters.

    Parameters:
        - data (list): List of dictionaries containing the data.

    Returns:
        - dict: Dictionary with keys as unique combinations and values as mean displacements.
    """
    avg_displacements = {}
    for key, group in groupby(data, key=lambda x: (x['experiment'], x['species'], x['pool_ID'], x['seq_number'])):
        group_list = [abs(float(item['angular_displacement'])) for item in group if item['angular_displacement'] and item['angular_displacement'] not in ['(None, None)', 'None']]
        if group_list:
            avg_displacements[key] = np.mean(group_list)
    return avg_displacements

def write_to_csv(data, file_path):
    """
    Write the processed data to a CSV file.

    Parameters:
        - data (list): List of dictionaries containing the data to be written.
        - file_path (str): Path where the CSV file should be saved.
    """
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Input and output file paths
    csv_path = "experiments/centroids_displacements.csv"
    output_path = "experiments/mean_angular_displacements_allowed.csv"

    # List of experiments that are allowed
    allowed_experiments = ["exp1_230509", "exp2_230516", "exp4_230523"]

    # Read the data from the CSV file
    data = read_csv(csv_path)

    # Filter the data based on allowed experiments
    filtered_data = filter_data_by_experiment(data, allowed_experiments)

    # Calculate the average displacements for the filtered data
    avg_displacements = calculate_mean_displacement(filtered_data)

    # Add the average displacements to the filtered data
    for row in filtered_data:
        key = (row['experiment'], row['species'], row['pool_ID'], row['seq_number'])
        row['avg_displacement'] = avg_displacements.get(key, 0)

    # Write the processed data to a new CSV file
    write_to_csv(filtered_data, output_path)
    print(f"Processed data saved to {output_path}")
