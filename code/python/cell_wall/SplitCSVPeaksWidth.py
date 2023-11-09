import csv
import os

# Set these paths as needed
directory_path = './input_directory'
output_directory = './output_directory'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):
        input_filepath = os.path.join(directory_path, filename)

        # Name the output files by appending "_peak.csv" and "_width.csv"
        peak_output_filepath = os.path.join(output_directory, filename.replace('.csv', '_peak.csv'))
        width_output_filepath = os.path.join(output_directory, filename.replace('.csv', '_width.csv'))

        with open(input_filepath, 'r') as infile:
            reader = csv.reader(infile)

            peak_rows = []
            width_rows = []

            # Extract the header
            header = next(reader)

            peak_headers = [col for col in header if col.startswith('Peak')]
            width_headers = [col for col in header if col.startswith('Width')]

            for row in reader:
                peak_data = [row[header.index(col)] for col in peak_headers]
                width_data = [row[header.index(col)] for col in width_headers]

                peak_rows.append(peak_data)
                width_rows.append(width_data)

            # Write the Peak data
            with open(peak_output_filepath, 'w', newline='') as peak_outfile:
                writer = csv.writer(peak_outfile)
                writer.writerow(peak_headers)
                writer.writerows(peak_rows)

            # Write the Width data
            with open(width_output_filepath, 'w', newline='') as width_outfile:
                writer = csv.writer(width_outfile)
                writer.writerow(width_headers)
                writer.writerows(width_rows)

            print(f"Data from {filename} split into '{peak_output_filepath}' and '{width_output_filepath}'")

print(f"Processing complete. Check the '{output_directory}' for the split files.")
