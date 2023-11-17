import os
import pandas as pd
import tifffile as tf
from PIL import Image

# Specify the path to the main directory
directory_path = "./experiment"

# Paths to the subfolders
tif_directory = "./experiment/tif" #This should be where your raw TIF files are stored
csv_directory = "./experiment/csv" #This should be where you've stored the CellProfiler output CSV files

# Output directory
output_directory = "./experiment/extracted"
# Get lists of all .tif and .csv files
tif_files = sorted([f for f in os.listdir(tif_directory) if f.endswith('.tif')])
csv_files = sorted([f for f in os.listdir(csv_directory) if f.endswith('.csv')])

# Check if the base names of the files match
assert all([tif_file[:-4] == csv_file[:-4] for tif_file, csv_file in zip(tif_files, csv_files)]), "File names do not match."

# Process each pair of TIF and CSV files
for tif_file, csv_file in zip(tif_files, csv_files):
    
    # Load CSV data
    df = pd.read_csv(os.path.join(csv_directory, csv_file))
    
    # Open the TIF file with tifffile
    with tf.TiffFile(os.path.join(tif_directory, tif_file)) as tif:
        original_image_array = tif.asarray()
        original_image = Image.fromarray(original_image_array)
        
        # Process each row in the CSV to extract cells
        for index, row in df.iterrows():
            x_coord = int(row['Location_Center_X'])
            y_coord = int(row['Location_Center_Y'])
            
            # Calculation used to determine side length
            side_length = int(row['AreaShape_Area']**0.5)
            
            left = x_coord - 50 - side_length // 2
            upper = y_coord - 50 - side_length // 2
            right = x_coord + 50 + side_length // 2
            lower = y_coord + 50 + side_length // 2
            
            # Extract the cell from the original image
            extracted_cell = original_image.crop((left, upper, right, lower))
            
            # Create an output directory for each TIF file to store extracted cells
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            # Save the extracted cell as a TIF file inside the output directory
            extracted_cell.save(os.path.join(output_directory, f'{tif_file[:-4]}_cell_{index}.tif'))
    
    print(f"Cells extracted for {csv_file}!")
