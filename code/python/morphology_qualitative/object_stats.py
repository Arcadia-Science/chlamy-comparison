"""
The script defines a function `compute_object_stats` that traverses a
base directory to locate and read CSV files containing object measurements.
For each of these files, it computes various statistical metrics such as
mean, maximum, mode, standard deviation, and median for the 'Object_ID'
column. It also extracts specific metadata. The computed statistics and
metadata are then merged with an existing CSV file, and the result is
saved as a new CSV file in the base directory. The function is executed
for a specific base directory defined as "./experiments".
"""

import os
import pandas as pd

def compute_object_stats(base_directory):
    # Create a list to store the results
    results = []

    # Walk through the base directory and process the CSV files in subdirectories
    for root, dirs, files in os.walk(base_directory):
        if '/objects/' in root and 'object_measurements.csv' in files:
            csv_path = os.path.join(root, 'object_measurements.csv')
            df = pd.read_csv(csv_path)

            # Compute the mean measurements for this CSV
            mean_object = df['Object_ID'].mean()
            max_object = df['Object_ID'].max()
            mode_object = df['Object_ID'].mode()[0]  # Mode returns a Series, take the first element
            std_object = df['Object_ID'].std()
            median_object = df['Object_ID'].median()

            # Extract metadata_species and metadata_pool_id from the CSV
            species = df['metadata_species'].iloc[0]
            pool_id = df['metadata_pool_id'].iloc[0]
            experiment_value = df['metadata_experiment'].iloc[0]

            # Append the data to the results list
            results.append({
                "metadata_experiment": experiment_value,
                "metadata_pool_id": pool_id,
                "metadata_species": species,
                "mean_object": mean_object,
                "max_object": max_object,
                "mode_object": mode_object,
                "std_object": std_object,
                "median_object": median_object
            })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results)

    # Load the existing CSV file into another DataFrame
    existing_df_path = os.path.join(base_directory, 'object_image_list_angles.csv')
    existing_df = pd.read_csv(existing_df_path)

    # Merge the existing DataFrame with the results DataFrame
    merged_df = pd.merge(
        existing_df,
        results_df,
        how="left",
        on=["metadata_experiment", "metadata_pool_id", "metadata_species"]
    )

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(os.path.join(base_directory, 'object_image_list_obj_stats.csv'), index=False)

#Entry point
if __name__ == "__main__":
    base_directory = "./experiments"
    compute_object_stats(base_directory)
