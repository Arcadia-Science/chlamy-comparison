# Phenotypic Analysis of Interfertile Algal Species

This repository contains code for image processing and analysis to compare phenotypes of interfertile *Chlamydomonas* species. These analyses are included in the publication [Phenotypic differences between interfertile Chlamydomonas species](https://doi.org/10.57844/arcadia-35f0-3e16).

![C. smithii is ~20% larger than C. reinhardtii](figs/morphology_2d.gif)

C. smithii is ~20% larger than C. reinhardtii


Release v2.1

Github

[![DOI](https://zenodo.org/badge/644048016.svg)](https://zenodo.org/badge/latestdoi/644048016)

Data Repository

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8326749.svg)](https://doi.org/10.5281/zenodo.8326749)

# Computational Protocols

For each step run the commands indicated in code blocks from the "chlamy-comparison" directory. This repository uses conda to manage software environments and installations.
You can find operating system-specific instructions for installing miniconda [here](https://docs.conda.io/en/latest/miniconda.html). We installed Miniconda3 version `23.7.3'.

                curl -JLO https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh # download the miniconda installation script
                bash Miniconda3-latest-Linux-x86_64.sh # run the miniconda installation script. Accept the license and follow the defaults.
                source ~/.bashrc # source the .bashrc for miniconda to be available in the environment

                # configure miniconda channel order
                conda config --add channels defaults
                conda config --add channels bioconda
                conda config --add channels conda-forge
                conda config --set channel_priority strict

## Getting started with this repository

After installing conda run the following command to create the pipeline run environment.


        conda env create -n morph2d --file envs/morph2d.yml
        conda activate morph2d


## Protocol for segmenting cells and taking measurements of 2D morphology

This protocol is a step by step computational guide to segment algal cells from video data. The input is video data of algal cells collected by brightfield or differential interference contrast microscopy. The output includes segmented cells as "objects" as well as measurements of the 2D morphology of the cells. For related experimental results [follow this link](https://research.arcadiascience.com/pub/result-chlamydomonas-phenotypes#nj8khdxj90e).

1. Download data from Zenodo. This will be a directory called "experiments" with subdirectories and image data. Use [zenodo_get](https://github.com/dvolgyes/zenodo_get).

        zenodo_get 10.5281/zenodo.8326749

2. Crop "pools" of swimming cells from raw videos using the [Fiji](https://imagej.net/software/fiji/) Macro batch_interactive_crop_savetif.v.0.0. Samples of raw videos are contained in the the "experiments/{experiment}/raw_sample" directories. Choose "experiments" as the input directory. [Link to Fiji macro](./code/FIJI/batch_interactive_crop_savetif.ijm)

3. Parse focal sequences of frames from "pools". [Link Python script](./code/python/morphology_2d/focus_filter_laplacian.py)

        python3 code/python/morphology_2d/focus_filter_laplacian.py

5. Sample the focal sequences randomly to generate a training set for pixel classification. [Link to Python script](./code/python/morphology_2d/sample_training_set.py)

        python3 code/python/morphology_2d/sample_training_set.py


6. Perform pixel classification with [Ilastik](https://www.ilastik.org/). Load the training sets and process the focal sequences in batch. Directory = main/experiments/ilastik

7. Organize probability maps by species and pool ID. [Link to Python script](./code/python/morphology_2d/organize_tif_by_species_and_well.py)

        python3 code/python/morphology_2d/organize_tif_by_species_and_well.py

8. **Python**: Segment cells and take 2D morphology measurements. [Link to Python script](./code/python/morphology_2d/segment_chlamy.py)

        python3 code/python/morphology_2d/segment_chlamy.py

   **Cellprofiler**: Alternatively, segment the cells and take measurements in Cellprofiler with the pipeline chlamy_segment.cppipe. [Link to Cellprofiler pipeline](code/CellProfiler/chlamy_segment.cppipe)

9.  Identify the maximal area measurement per focal sequence. [Link to Python script](./code/python/morphology_2d/max_area_focus_seq.py)

        python3 code/python/morphology_2d/max_area_focus_seq.py

10.  Parse per pool mean measurements. [Link to Python script](./code/python/morphology_2d/parse_2d_morphology.py)

        python3 code/python/morphology_2d/parse_2d_morphology.py


## Script for generating vector graphics of idealized cell

This script will generate a vector graphic of an idealized cell. The user may define the 2D morphology measurements in the script. The output is a vector graphic. For related results [follow this link](https://research.arcadiascience.com/pub/result-chlamydomonas-phenotypes#nj8khdxj90e). [Link to Python script](./code/python/idealized_cell/chlamy_modeler.py)

    python3 code/python/idealized_cell/chlamy_modeler.py

## Protocol for visual assessments of cell morphology

This protocol is a step by step computational guide to create panels of a video to display difference in the 2D morphology of interfertile algal species. The protocol follows upon the previous protocols in this document. The input is video data of algal cells collected by brightfield or differential interference contrast microscopy, as well as object masks. The output includes videos of masked cells and cumulative average projections of cells. For related results [follow this link](https://research.arcadiascience.com/pub/result-chlamydomonas-phenotypes#nsmnfifz9no).


1. Creat a list of images with maximum area objects with relevant metadata. [Link to Python script](./code/python/morphology_qualitative/max_area_image_object_list.py)

        python3 code/python/morphology_qualitative/max_area_image_object_list.py

2. Identify image frames to calculate swim angle. [Link to Python script](./code/python/morphology_qualitative/frames_for_angle.py)

        python3 code/python/morphology_qualitative/frames_for_angle.py

3. Calculate swim angle and swim angle relative to the Y-axis. [Link to Python script](./code/python/morphology_qualitative/swim_angle.py)

       python3 ./code/python/morphology_qualitative/swim_angle.py

4. Mask cells. [Link to Python script](./code/python/morphology_qualitative/image_mask.py)

       python3 code/python/morphology_qualitative/image_mask.py

5. Get statistics about the objects. [Link to Python script](./code/python/morphology_qualitative/object_stats.py)

       python3 code/python/morphology_qualitative/object_stats.py

6. Crop and reorient cells so they are swimming "up" and the major axis of the cell is aligned with the y-axis. [Link to Python script](./code/python/morphology_qualitative/crop_orient_major.py)

        python3 code/python/morphology_qualitative/crop_orient_major.py

7. Combine cells into stacks by experiment and species. [Link to Python script](./code/python/morphology_qualitative/save_stack.py)

        python3 code/python/morphology_qualitative/save_stack.py

8.  Create a substack with the number of frames you want in the final video in [Fiji](https://imagej.net/software/fiji/).

9.  Calculate cumulative average projections from the substacks with the Fiji macro batch_sequential_avg_projection.ijm. [Link to Fiji macro](./code/FIJI/batch_sequential_avg_projection.ijm)

## Protocol for measurement and visual assessment of cell motility

![C. reinhardtii swims faster and they have different and complex modes of motility](figs/fig_motility_dynamic.gif)

1. Activate the environment with conda.

     conda env create -n motility --file envs/motility.yml
     conda activate motility
   
2. Download data from Zenodo. This will be a directory called "experiments" with subdirectories and image data. **Skip this step if data is already downloaded.** Use [zenodo_get](https://github.com/dvolgyes/zenodo_get).

        zenodo_get 10.5281/zenodo.8326749

3. Collect information about objects. The script processes a set of images, identifies objects in them, calculates their centroids, and determines the movement direction of the largest object by comparing the centroids between frames. **Input** = cell objects. **Output** = image_data_with_upward_angles.csv file. [Link to script](./code/python/motility_dynamic_fig/object_trajectory_info.py)

        python3 code/python/motility_dynamic_fig/object_trajectory_info.py

4. Reorient objects. The script processes images based on data in the CSV file. It rotates, translates, and crops each image based on the movement direction of a detected object. The processed images are then saved in new directories, ".../final_transformed_images/...". **Input** = objects and image_data_with_upward_angles.csv. **Output** = transformed images. [Link to script](./code/python/motility_dynamic_fig/rotate_translate.py)

        python3 code/python/motility_dynamic_fig/rotate_translate.py

5. Calculate angular and linear displacement from frame to frame. The script processes images, identifies contours, and computes both angular (degrees) and linear (pixels) displacements between contours in consecutive frames. The angle is calculated as the angle between two vectors defined by three consecutive points. The linear displacement is the distance between point two and three. The displacements are listed under the third point. The results are saved to a CSV file. **Input** = images in final_transformed_images directories. **Output** = centroids_displacements.csv. In these images 1 pixel = 0.6398 microns. [Link to script](./code/python/motility_dynamic_fig/angular_linear_displacement.py)

        python3 code/python/motility_dynamic_fig/angular_linear_displacement.py

6. Calculate the mean absolute angular displacement per track. Only include allowed experiments. Experiment 3 was removed due to external flow through the wells. **Input** = centroids_displacements.csv. **Output** = mean_angular_displacements_allowed.csv. [Link to script](./code/python/motility_dynamic_fig/mean_per_track_allowed_experiments.py)

        python3 code/python/motility_dynamic_fig/mean_per_track_allowed_experiments.py

7. Filter data. This script filters rows from an input CSV file where the 'seq_frame' column has a value of 0 and writes the filtered data to an output CSV file. **Input** = mean_angular_displacements_allowed.csv. **Output** = filtered_unbinned_data.csv. [Link to script](./code/python/motility_dynamic_fig/filter_data.py)

        python3 code/python/motility_dynamic_fig/filter_data.py

8. Sample filtered data to ensure equal representation of each species for each experiment. This script samples rows from an input CSV file, ensuring that each combination of 'experiment' and 'species' in the dataset is represented by the same number of rows. This number is determined by the smallest group size of the combinations. The sampled data is then written to an output CSV file. **Input** = filtered_unbinned_data.csv. **Output** = sampled_unbinned_data.csv. [Link to script](./code/python/motility_dynamic_fig/sample_filtered_data.py)

        python3 code/python/motility_dynamic_fig/sample_filtered_data.py

9. Bin the sampled data into 18 bins representing 10 degree spans between 0 and 180 degrees. This script reads data from an input CSV file, bins the 'avg_displacement' values into 18 bins,and assigns each row a bin number based on its 'avg_displacement' value. The binned data is then written to an output CSV file.  **Input** = sampled_unbinned_data.csv. **Output** = sampled_binned_data.csv. [Link to script](./code/python/motility_dynamic_fig/bin_sampled_data.py)

        python3 code/python/motility_dynamic_fig/bin_sampled_data.py

10. Merge data into one csv file. This script merges two input CSV files (`sampled_binned_data.csv` and `centroids_displacements.csv`) based on common columns ('experiment', 'species', 'pool_ID', and 'seq_number'). After merging, it retains specific columns from the sampled file and all columns from the centroids file. The merged data is then written to an output CSV file. **Inputs** = sampled_binned_data.csv and  centroids_displacements.csv. **Output** = merged_data.csv. [Link to script](./code/python/motility_dynamic_fig/merged_data.csv)

        python3 code/python/motility_dynamic_fig/parse_sampled_binned_sequences.py experiments/sampled_binned_data.csv experiments/centroids_displacements.csv experiments/merged_data.csv

11. Plot histogram with bins and generate vector tracks. This script performs multiple visualization tasks on data read from a CSV file named 'merged_data.csv'. First, it creates and saves vector plots for different groups in the data, with each plot displaying a vector and an associated average angular velocity. Then, it generates a histogram displaying the frequency of bins by species for seq_frame=0. The vector plots are saved as grayscale 8-bit TIFF images in specific directories, and the histogram is saved as a PNG. **Input** = merged_data.csv. **Output** = Images of vector tracks saved in directories as such, "./experiments/vectors_sampled_binned/bin_{bin_category}/{species}/". [Link to script](./code/python/motility_dynamic_fig/plot_histogram_vector_images.py)

        python3 code/python/plot_histogram_vector_images.py

## Cell Wall Analysis: Protocol for measuring cell wall thickness

This protocol is a step-by-step computational guide to analyze the intensity and diameter of calcofluor-white signal marking the cell wall of Chlamydomonas species. The input is single-frame, greyscale 16-bit .tif files of the medial z-plane of fixed and stained algal cells collected by spinning disk microscopy through standard DAPI settings. These images are available on [Zenodo]([10.5281/zenodo.10127618](https://doi.org/10.5281/zenodo.10127618)). The output includes images of marked cells and raw intensity values through the max axis and the min axis. For related results [follow this link](https://research.arcadiascience.com/pub/result-chlamydomonas-phenotypes#nsmnfifz9no). 


In Step 1, use the zipped folder downloaded from Zenodo as input to Cell Profiler.  Our python code assumes you export the .csv files generated in Cell Profiler to a folder titled "experiment"
1. Segment & Measure cells in Cell Profiler using [CW_Pipeline.cppipe](./code/CellProfiler/CW_Pipeline.cppipe)


2. Extract individual cells from larger files using the cell position coordinates from the Cell Profiler segmentation using [ExtractIndividualCells.py](./code/python/cell_wall/ExtractIndividualCells.py)

3. Re-segment cells & measure objects in Cell Profiler: Use this updated pipeline that provides the same coordinate & orientation measurements but is adapted for larger datasets (pipeline [CW_Pipeline_Extracted.cppipe](./code/CellProfiler/CW_Pipeline_Extracted.cppipe)

4. Convert Database to CSV since Cell Profiler doesn't allow exporting large .csv files ([SQLite2CSV.py](code/python/cell_wall/SQLite2CSV.py))


4. Use the new cell coordinates of extracted cells to realign extracted cells to to have the major axis parallel with the image frame. Afterwards, I manually moved the files with the "_aligned" suffix to their own subfolder titled "aligned" ([AlignExtractedObjects.py](code/python/cell_wall/AlignExtractedObjects.py)).


5. Add additional empty pixels to the side of each "aligned" .tif of the extracted cells so that each extracted image is the same dimension without resizing the actual image. Afterwards, I manually moved the files with the "padded_" prefix to their own subfolder titled "padded" ([PadExtractedTiffs.py](code/python/cell_wall/PadExtractedTiffs.py)).

6. Measure 5 pixel wide line scans through the major and minor axes of the "padded" images. This data is exported to a .csv file and produces a marked up image of the input .tif depicting where the measurement occured ([RadialIntensityMajorMinor.py](code/python/cell_wall/RadialIntensityMajorMinor.py)).

7. Extract the peak values from the line scan data to calculate intensity and width. "processed_" files were then manually moved to a "processed" subfolder ([PeakAndWidthExtractor.py](code/python/cell_wall/PeakAndWidthExtractor.py))


8. Split data between peaks and width ([SplitCSVPeaksWidth.py](code/python/cell_wall/SplitCSVPeaksWidth.py)).

Data output from here was imported into GraphPad Prism for visualization and 2way ANOVA calculations.

# Versions and platforms

*Fiji macro* was used with ImageJ2 Version 2.14.0/1.54f

*Python* code was run with Python 3.11.5

Computation was performed on MacBook Pro computer with the following specifications:

macOS: Ventura 13.4.1 (c)
Chip Apple M2 Max
Memory 32 Gb

# Feedback, contributions, and reuse

See [this guide](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md) to see how we recognize feedback and contributions on our code.