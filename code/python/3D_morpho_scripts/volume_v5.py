import SimpleITK as sitk
import os
import csv

SCALING_FACTOR = 43.0769 # pixels/micron for 1.5x magnifier
#SCALING_FACTOR = 64.6154  # pixels/micron for 1.0x magnifier
Z_STEP = 0.1  # in microns

def compute_volume_and_density(mask_image, raw_image):
    """
    Compute the volume of the segmented structure in the mask, the integrated density, and the mean intensity.

    :param mask_image: SimpleITK.Image object representing the 3D mask.
    :param raw_image: SimpleITK.Image object representing the 3D raw data.
    :return: Tuple containing volume, integrated density, and mean intensity.
    """
    mask_array = sitk.GetArrayFromImage(mask_image)
    raw_array = sitk.GetArrayFromImage(raw_image)

    non_zero_voxel_count = mask_array.nonzero()[0].shape[0]
    voxel_size = mask_image.GetSpacing()[0] * mask_image.GetSpacing()[1] * Z_STEP
    volume = non_zero_voxel_count * voxel_size

    integrated_density = raw_array[mask_array.nonzero()].sum()

    mean_intensity = integrated_density / non_zero_voxel_count if non_zero_voxel_count != 0 else 0

    return volume, integrated_density, mean_intensity

def convert_pixel_volume_to_micron(volume_in_pixels):
    """Convert volume from pixels^3 to microns^3."""
    return volume_in_pixels / (SCALING_FACTOR ** 2)

def read_images(mask_path, raw_data_path):
    """Read the mask and raw data images."""
    try:
        mask_image = sitk.ReadImage(mask_path)
        raw_data_image = sitk.ReadImage(raw_data_path)
        return mask_image, raw_data_image
    except Exception as e:
        print(f"Error reading images: {e}")
        return None, None

def main(mask_directory, raw_data_directory):
    total_volume_pixels = 0.0
    total_density = 0.0
    total_non_zero_voxels = 0  # Count of all non-zero voxels across all images

    mask_files = [f for f in os.listdir(mask_directory) if f.endswith("_BGSub.segmentation.tiff")]
    raw_data_files = os.listdir(raw_data_directory)

    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Mask File", "Volume (cubic microns)", "Integrated Density", "Mean Intensity"])

        for mask_file_name in mask_files:
            expected_raw_data_filename = mask_file_name.replace("processed_", "").replace("_BGSub.segmentation.tiff", ".tif")
            mask_path = os.path.join(mask_directory, mask_file_name)

            if expected_raw_data_filename not in raw_data_files:
                print(f"No matching raw data for mask file: {mask_file_name}")
                continue

            raw_data_path = os.path.join(raw_data_directory, expected_raw_data_filename)
            mask_image, raw_data_image = read_images(mask_path, raw_data_path)

            if mask_image is None or raw_data_image is None:
                continue

            volume_in_pixels, integrated_density, mean_intensity = compute_volume_and_density(mask_image, raw_data_image)
            volume_in_microns = convert_pixel_volume_to_micron(volume_in_pixels)

            csv_writer.writerow([mask_file_name, volume_in_microns, integrated_density, mean_intensity])

            total_volume_pixels += volume_in_pixels
            total_density += integrated_density
            total_non_zero_voxels += volume_in_pixels / (mask_image.GetSpacing()[0] * mask_image.GetSpacing()[1] * Z_STEP)

    total_volume_microns = convert_pixel_volume_to_micron(total_volume_pixels)
    overall_mean_intensity = total_density / total_non_zero_voxels if total_non_zero_voxels != 0 else 0

    print(f"\nTotal segmented volume: {total_volume_microns:.2f} cubic microns")
    print(f"Total integrated density: {total_density:.2f} (unit depends on the raw data)")
    print(f"Overall mean intensity: {overall_mean_intensity:.2f}")

if __name__ == "__main__":
    mask_directory = input("Enter the path to the directory containing 3D image masks: ")
    raw_data_directory = input("Enter the path to the directory containing the raw data: ")
    main(mask_directory, raw_data_directory)
