"""
This Python script reads multiple CSV files located in a directory structure
 to find the object with the maximum 'Area' for each unique 'metadata_sequence'.
 It then copies the associated image of that object to a new directory and appends
 or creates a new CSV file containing information about the object.
 The script uses the pandas library for data manipulation and the `os`
 and `shutil` libraries for file and directory operations.
"""

import shutil
import os
import pandas as pd

def extract_max_area_object(base_directory):
    """Extracts and saves the object with the maximal area for each unique sequence in each CSV file."""

    # Walk through the base directory and process the CSV files
    for root, dirs, files in os.walk(base_directory):
        if '/objects/' in root and 'object_measurements.csv' in files:
            csv_path = os.path.join(root, 'object_measurements.csv')
            df = pd.read_csv(csv_path)

            print(f"Processing: {csv_path}")  # Debug: Show which file is being processed
            print("Columns in CSV:", df.columns)  # Debug: Show columns

            if 'metadata_sequence' not in df.columns:
                print(f"Skipping file {csv_path} as it doesn't contain 'metadata_sequence' column.")
                continue  # Skip the current iteration and proceed to the next file


            # Group the data by the sequence and extract the row with max area for each group
            idx = df.groupby(['metadata_sequence'])['Area'].idxmax()

            # Subset the dataframe to include only the rows with maximum areas in their respective groups
            max_area_df = df.loc[idx]

            for _, max_area_row in max_area_df.iterrows():
                # Source image path for the object
                src_frame_path = os.path.join(root, max_area_row['Image'])

                # Destination path for the object
                dest_directory = os.path.join(base_directory, max_area_row['metadata_experiment'], 'max_area',
                                              max_area_row['metadata_species'], max_area_row['metadata_pool_id'])
                os.makedirs(dest_directory, exist_ok=True)

                # Copy the image to the destination directory
                shutil.copy(src_frame_path, dest_directory)

                # Destination CSV path
                csv_dest_path = os.path.join(dest_directory, 'max_area_data.csv')

                # Check if the CSV file exists to decide whether to write headers
                if os.path.exists(csv_dest_path):
                    # If CSV exists, append without the header
                    max_area_row.to_frame().T.to_csv(csv_dest_path, mode='a', header=False, index=False)
                else:
                    # If CSV doesn't exist, create it and write with the header
                    max_area_row.to_frame().T.to_csv(csv_dest_path, mode='w', header=True, index=False)

# Entry point
if __name__ == "__main__":
    base_directory = "./experiments"  # Adjust this to the base directory path
    extract_max_area_object(base_directory)
