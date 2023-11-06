"""
Summary:
    This script filters rows from an input CSV file where the 'seq_frame' column has a value of 0
    and writes the filtered data to an output CSV file.

Inputs:
    input_csv_path: Path to the input CSV file.
    output_csv_path: Path to the output CSV file where filtered data will be saved.

Outputs:
    A new CSV file with rows where the 'seq_frame' column has a value of 0.

Entry Point:
    The script starts its execution from the `if __name__ == "__main__":` block.
"""

import csv

def filter_csv_by_seq_frame(input_csv_path, output_csv_path):
    """
    Filters rows from an input CSV file where the 'seq_frame' column is 0
    and writes the filtered rows to an output CSV file.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_csv_path (str): Path to the output CSV file.

    """

    # Open the input and output CSV files.
    with open(input_csv_path, 'r') as infile, open(output_csv_path, 'w', newline='') as outfile:
        # Initialize CSV DictReader and DictWriter objects
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        # Write the header to the output CSV
        writer.writeheader()

        # Iterate through each row in the input CSV
        for row in reader:
            # Check if 'seq_frame' column value is '0'
            if row['seq_frame'] == '0':
                # Write the row to the output CSV
                writer.writerow(row)

    # Print the path to the saved filtered data
    print(f"Filtered data saved to {output_csv_path}")

# Entry point of the script
if __name__ == "__main__":
    # Define input and output paths
    input_path = 'experiments/mean_angular_displacements_allowed.csv'
    output_path = 'experiments/filtered_unbinned_data.csv'

    # Call the filter function with the defined paths
    filter_csv_by_seq_frame(input_path, output_path)
