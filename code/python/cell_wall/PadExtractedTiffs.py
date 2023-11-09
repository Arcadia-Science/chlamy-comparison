from PIL import Image
import os

def pad_image(img, target_width, target_height, fill_value=0):
    width, height = img.size
    pad_width = (target_width - width) // 2
    pad_height = (target_height - height) // 2

    new_img = Image.new("I;16", (target_width, target_height), fill_value)
    new_img.paste(img, (pad_width, pad_height))
    
    return new_img

def process_images_in_directory(directory):
    tif_files = [f for f in os.listdir(directory) if f.endswith('.tif')]

    max_width = 0
    max_height = 0

    # First pass: Determine max width and height
    for file in tif_files:
        with Image.open(os.path.join(directory, file)) as img:
            width, height = img.size
            max_width = max(max_width, width)
            max_height = max(max_height, height)

    # Second pass: Pad and save each image
    for file in tif_files:
        with Image.open(os.path.join(directory, file)) as img:
            padded_image = pad_image(img, max_width, max_height)
            padded_image.save(os.path.join(directory, "padded_" + file))

if __name__ == "__main__":
    dir_path = '/path/to/your/directory'  # change this to your directory path
    process_images_in_directory(dir_path)
