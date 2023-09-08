"""
The script defines a function `object_list` that takes a `base_directory`
as an argument and scans through its subdirectories to find and
process CSV files located in any folder named `max_area`.
When a `max_area_data.csv` file is found, the script reads it into a Pandas DataFrame,
performs several column calculations based on existing columns,
and then appends this processed data to an overall DataFrame.
Finally, the script saves the aggregated DataFrame into a new CSV file
called `object_image_list.csv` in the `base_directory`.
"""
import os
import pandas as pd

def object_list(base_directory):
    # Create an empty DataFrame to store all the results
    all_data = pd.DataFrame()

    # Walk through the base directory and process the CSV files in subdirectories
    for root, dirs, files in os.walk(base_directory):
        if '/max_area/' in root and 'max_area_data.csv' in files:
            csv_path = os.path.join(root, 'max_area_data.csv')
            df = pd.read_csv(csv_path)

            # Calculate the 'seq_frame' column based on the 'Image' column
            df['seq_frame'] = df['Image'].apply(lambda x: x.split("_")[-1].split(".")[0])

            # Calculate the 'first_seq_frame' column based on the 'metadata_frames' column
            df['first_seq_frame'] = df['metadata_frames'].apply(lambda x: x.split("to")[0])

            # Calculate the 'image_frame' column based on 'seq_frame' and 'first_seq_frame'
            df['image_frame'] = df['seq_frame'].astype(int) + df['first_seq_frame'].astype(int)

            # Calculate the 'well_name' column based on the 'Image' column
            df['well_name'] = df['Image'].apply(lambda x: x.split("_seq")[0] + ".tif")

            # Append the data to the overall DataFrame
            all_data = pd.concat([all_data, df], ignore_index=True)

    # Save the aggregated DataFrame to a new CSV file
    all_data.to_csv(os.path.join(base_directory, 'object_image_list.csv'), index=False)

if __name__ == "__main__":
    base_directory = "./experiments"
    object_list(base_directory)
