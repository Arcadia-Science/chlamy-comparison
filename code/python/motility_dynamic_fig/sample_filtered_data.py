"""
Summary:
    This script samples rows from an input CSV file, ensuring that each combination of 'experiment'
    and 'species' in the dataset is represented by the same number of rows. This number is determined
    by the smallest group size of the combinations. The sampled data is then written to an output CSV file.

Inputs:
    input_csv_path: Path to the input CSV file.
    output_csv_path: Path to the output CSV file where sampled data will be saved.

Outputs:
    A new CSV file with sampled data ensuring equal representation for each 'experiment' and 'species' combination.

Entry Point:
    The script starts its execution from the `if __name__ == "__main__":` block.
"""

import csv
import random
from collections import defaultdict

def sample_csv_by_experiment_and_species(input_csv_path, output_csv_path):
    """
    Samples rows from an input CSV file ensuring each combination of 'experiment' and 'species'
    is represented by the same number of rows.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_csv_path (str): Path to the output CSV file.

    """

    # Load data from input CSV
    with open(input_csv_path, 'r') as infile:
        reader = csv.DictReader(infile)
        data = [row for row in reader]

    # Group data by 'experiment' and 'species' columns
    grouped_data = defaultdict(list)
    for row in data:
        key = (row['experiment'], row['species'])
        grouped_data[key].append(row)

    # Determine the number of samples based on the smallest group size
    min_group_size = min(len(group) for group in grouped_data.values())

    # Sample data ensuring equal representation for each combination
    sampled_data = []
    for group in grouped_data.values():
        sampled_data.extend(random.sample(group, min_group_size))

    # Save the sampled data to output CSV
    with open(output_csv_path, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(sampled_data)

    # Print the path to the saved sampled data
    print(f"Sampled data saved to {output_csv_path}")

# Entry point of the script
if __name__ == "__main__":
    # Define input and output paths
    input_path = 'experiments/filtered_unbinned_data.csv'
    output_path = 'experiments/sampled_unbinned_data.csv'

    # Call the sampling function with the defined paths
    sample_csv_by_experiment_and_species(input_path, output_path)
