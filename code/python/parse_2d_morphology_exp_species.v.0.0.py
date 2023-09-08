"""
This Python script navigates through a directory structure
to locate CSV files containing various measurements of objects,
including their areas, eccentricities, and other geometric features.
For each CSV file, it computes the mean values for these measurements and
extracts associated metadata like species and pool ID.
Finally, it aggregates all these calculated means and metadata into a new CSV file,
which is saved in the base directory.
"""

import os
import pandas as pd

def compute_area_means(base_directory):
    # Create a list to store the results
    results = []

    # Walk through the base directory and process the CSV files in subdirectories
    for root, dirs, files in os.walk(base_directory):
        if '/max_area/' in root and 'max_area_data.csv' in files:
            csv_path = os.path.join(root, 'max_area_data.csv')
            df = pd.read_csv(csv_path)

            # Compute the mean measurements for this CSV
            mean_area = df['Area'].mean()
            mean_eccentricity = df['Eccentricity'].mean()
            mean_perimeter = df['Perimeter'].mean()
            mean_major_axis_length = df['MajorAxisLength'].mean()
            mean_minor_axis_length = df['MinorAxisLength'].mean()



            # Extract metadata_species and metadata_pool_id from the CSV
            species = df['metadata_species'].iloc[0]  # Assuming all rows have the same species
            pool_id = df['metadata_pool_id'].iloc[0]  # Assuming all rows have the same pool_id
            experiment_value = df['metadata_experiment'].iloc[0]

            # Append the data to the results list
            results.append({
                "experiment": experiment_value,
                "pool_id": pool_id,
                "species": species,
                "mean_area": mean_area,
                "mean_eccentricity": mean_eccentricity,
                "mean_major_axis_length": mean_major_axis_length,
                "mean_minor_axis_length": mean_minor_axis_length,
                "mean_perimeter": mean_perimeter
            })

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results)

    # Save the results to a CSV file
    results_df.to_csv(os.path.join(base_directory, 'measure_2d_exp_species.v.1.csv'), index=False)

if __name__ == "__main__":
    base_directory = "./experiments"
    compute_area_means(base_directory)
