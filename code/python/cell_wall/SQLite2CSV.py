import sqlite3
import csv
from collections import defaultdict

# Function to extract the base image name
def extract_image_name(full_name):
    parts = full_name.split('_cell_')
    return parts[0] + '.tif'

# Connect to the SQLite database
db_path = './experiment/extracted'  # Path to where the SQLite database from the second Cell Profiler run is
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Fetch all rows from the table
table_name = 'MyExpt_Per_Image' 
cursor.execute(f"SELECT * FROM {table_name}")
rows = cursor.fetchall()

# Group rows by image name
grouped_data = defaultdict(list)
column_index = 9  # REPLACE with the index of 'Image_FileName_AllExtractedImages' in your table
for row in rows:
    image_name = extract_image_name(row[column_index])
    grouped_data[image_name].append(row)

# Export each group to a separate CSV file
for image_name, data in grouped_data.items():
    with open(f"{image_name}.csv", 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write the headers first
        writer.writerow([description[0] for description in cursor.description])

        # Write the content
        writer.writerows(data)

# Close the SQLite connection
connection.close()
