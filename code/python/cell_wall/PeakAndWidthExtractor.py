import pandas as pd
from scipy.signal import find_peaks, peak_widths
import os

def process_row(row):
    try:
        # Ensure the row contains only numeric data
        numeric_row = row.dropna().astype(float)
        # Find peaks and their properties
        peaks, properties = find_peaks(numeric_row, height=0)
        # Extract peak intensities
        peak_intensities = properties['peak_heights']
        # Calculate widths at half maxima
        widths_at_half_max = peak_widths(numeric_row, peaks, rel_height=0.5)
        # We only want the widths, not the other details
        half_maxima_widths = widths_at_half_max[0]
        return peak_intensities, half_maxima_widths
    except ValueError:
        return [], []

def process_file(file_path):
    # Load the data
    df = pd.read_csv(file_path)
    # Create containers for the peak and width data
    peak_data = []
    width_data = []
    # Process each row and collect the peak and width data
    for _, row in df.iterrows():
        peak_intensities, half_maxima_widths = process_row(row[1:])  # Exclude 'Cell #' column
        peak_data.append(peak_intensities)
        width_data.append(half_maxima_widths)
    # Determine the maximum number of peaks/widths found
    max_peaks = max(len(peak) for peak in peak_data)
    max_widths = max(len(width) for width in width_data)
    # Create new columns for each peak and width
    for i in range(max_peaks):
        df[f'Peak_{i+1}'] = [peak[i] if i < len(peak) else None for peak in peak_data]
    for i in range(max_widths):
        df[f'Width_{i+1}'] = [width[i] if i < len(width) else None for width in width_data]
    # Determine the output file path
    output_file_path = os.path.join(os.path.dirname(file_path), f'processed_{os.path.basename(file_path)}')
    # Save the transformed data to a new CSV file
    df.to_csv(output_file_path, index=False)

def process_all_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)

# Specify the folder containing the CSV files
folder_path = './experiment/extracted/tif/aligned/padded/csv'

# Process all CSV files in the specified folder
process_all_files(folder_path)
