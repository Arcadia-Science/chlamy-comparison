"""
Summary:
    This script merges two input CSV files (`sampled_file` and `centroids_file`) based on common columns
    ('experiment', 'species', 'pool_ID', and 'seq_number'). After merging, it retains specific columns
    from the sampled file and all columns from the centroids file. The merged data is then written to an
    output CSV file.

Inputs:
    sampled_file: Path to the sampled data CSV file.
    centroids_file: Path to the centroids data CSV file.
    output_file: Path where the merged CSV file will be saved.

Outputs:
    A new CSV file containing the merged data from the two input CSV files.

Entry Point:
    The script starts its execution from the `if __name__ == '__main__':` block. It accepts command-line
    arguments for the paths of the input and output files.
"""

import pandas as pd
import argparse

def filter_and_save_data(sampled_file, centroids_file, output_file):
    """
    Merges data from two input CSV files based on common columns and writes the merged data to an output CSV file.

    Args:
        sampled_file (str): Path to the sampled data CSV file.
        centroids_file (str): Path to the centroids data CSV file.
        output_file (str): Path where the merged CSV file will be saved.

    """

    # Load both CSV files into pandas DataFrames
    sampled_data = pd.read_csv(sampled_file)
    centroids_data = pd.read_csv(centroids_file)

    # Merge the two DataFrames based on the specified columns
    # and retain specific columns from the sampled data and all columns from the centroids data
    merged_data = pd.merge(sampled_data[['experiment', 'species', 'pool_ID', 'seq_number', 'avg_displacement', 'bin']],
                           centroids_data,
                           on=['experiment', 'species', 'pool_ID', 'seq_number'],
                           how='inner')

    # Save the merged data to a new CSV file
    merged_data.to_csv(output_file, index=False)

# Entry point of the script
if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(description='Merge CSV files based on given columns.')
    parser.add_argument('sampled_file', type=str, help='Path to the sampled data CSV file.')
    parser.add_argument('centroids_file', type=str, help='Path to the centroids data CSV file.')
    parser.add_argument('output_file', type=str, help='Path where the merged CSV file will be saved.')

    # Parse command-line arguments
    args = parser.parse_args()

    # Call the merge function with the parsed arguments
    filter_and_save_data(args.sampled_file, args.centroids_file, args.output_file)
