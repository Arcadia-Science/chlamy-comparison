import os
import numpy as np
import csv
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def extract_intensity_profile(img, start, end, thickness=5):
    intensities = []
    width, height = img.size
    for i in np.linspace(0, 1, max(width, height)):
        x = int((1 - i) * start[0] + i * end[0])
        y = int((1 - i) * start[1] + i * end[1])
        x_range = [j for j in range(-thickness // 2, thickness // 2 + 1) if 0 <= x + j < width]
        y_range = [k for k in range(-thickness // 2, thickness // 2 + 1) if 0 <= y + k < height]
        intensity = np.mean([img.getpixel((x + j, y + k)) for j in x_range for k in y_range])
        intensities.append(intensity)

    return intensities

def process_images_in_directory(directory, prefixes=None, output_directory=None):
    if prefixes is None:
        prefixes = [""]  # Empty prefix will match all files
    if output_directory is None:
        output_directory = os.path.join(directory, 'Output')
        os.makedirs(output_directory, exist_ok=True)
    
    tif_files = [f for f in os.listdir(directory) if f.endswith('.tif') and any(prefix in f for prefix in prefixes)]
    
    data_storage_major = {prefix: [["Cell #"] + [f"Position {i}" for i in range(81, 421)]] for prefix in prefixes}
    data_storage_minor = {prefix: [["Cell #"] + [f"Position {i}" for i in range(81, 421)]] for prefix in prefixes}
    
    for file in tif_files:
        prefix = next((p for p in prefixes if p in file), "")
        
        with Image.open(os.path.join(directory, file)) as img:
            width, height = img.size
            
            start_major = (width // 2, 0)
            end_major = (width // 2, height)
            major_intensities = extract_intensity_profile(img, start_major, end_major)
            
            start_minor = (0, height // 2)
            end_minor = (width, height // 2)
            minor_intensities = extract_intensity_profile(img, start_minor, end_minor)

            marked_img = img.copy()
            draw = ImageDraw.Draw(marked_img)
            draw.line([start_major, end_major], width=5, fill=65535)
            draw.line([start_minor, end_minor], width=5, fill=65535)
            marked_img.save(os.path.join(output_directory, "Marked", file))
            
            data_storage_major[prefix].append([f"Cell {file} (Major)"] + major_intensities[80:-80])
            data_storage_minor[prefix].append([f"Cell {file} (Minor)"] + minor_intensities[80:-80])
    
    for prefix, data in data_storage_major.items():
        with open(os.path.join(output_directory, f'{prefix}_major_axis_data.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    for prefix, data in data_storage_minor.items():
        with open(os.path.join(output_directory, f'{prefix}_minor_axis_data.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    
    for prefix in prefixes:
        major_intensities = np.array([row[1:] for row in data_storage_major[prefix][1:]])
        minor_intensities = np.array([row[1:] for row in data_storage_minor[prefix][1:]])
        
        mean_major = np.mean(major_intensities, axis=0)
        mean_minor = np.mean(minor_intensities, axis=0)
        
        plt.figure(figsize=(12, 6))
        plt.plot(mean_major, label='Major Axis')
        plt.plot(mean_minor, label='Minor Axis')
        plt.title(f'Mean Intensity Profile for {prefix}')
        plt.legend()
        plt.xlabel('Position')
        plt.ylabel('Intensity')
        plt.savefig(os.path.join(output_directory, f'Mean_Profile_{prefix}.png'))
        plt.show()

if __name__ == "__main__":
    directory_path = './experiment/extracted/tif/padded' 
    output_directory_path = './experiment/extracted/tif/padded/marked'
    prefix_input = 'padded'
    prefixes_list = None if prefix_input == '' else prefix_input.split(',')
    process_images_in_directory(directory_path, prefixes=prefixes_list, output_directory=output_directory_path)
