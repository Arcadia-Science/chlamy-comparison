# Phenotypic Analysis of Interfertile Algal Species

This repository contains code for image processing and analysis to compare phenotypes of interfertile *Chlamydomonas* species. These analyses are included in the publication [Phenotypic differences between interfertile Chlamydomonas species](https://doi.org/10.57844/arcadia-35f0-3e16).

![C. smithii is ~20% larger than C. reinhardtii](morphology_2d.gif)

C. smithii is ~20% larger than C. reinhardtii


Release v4

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

For creating the pipeline run environment for 3D morphology run the following commands:


        conda env create -n morph3d --file envs/morph3d.yml
        conda activate morph3d


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

## Protocol for visual and qualitative assessments of cell morphology

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

# 3D morphology protocols

This protocol is a step by step computational protocol to process and analyze the 3D morphology of the mitochondiral and cholorplast network of algal cells. The input is sub-nyquist sampled z-stacks of algal cells acquired by spinning disk confocal microscopy. The output includes images that have been deconvolved, accompanying segmentation masks of the labeled data and volume measurements. For related results [follow this link](https://research.arcadiascience.com/pub/result-chlamydomonas-phenotypes#nsmnfifz9no).

1. Download demo data from Zenodo. This will be a directory called "3D_morpho" with subdirectories and image data. Use [zenodo_get](https://github.com/dvolgyes/zenodo_get). (link TBD)

## Processing raw data

You will need to install 2 FIJI plugins to be able to process images in the following sections of the protocol that utilize FIJI for image processing. Download DeconvolutionLab2 (https://bigwww.epfl.ch/deconvolution/deconvolutionlab2/) and PSF Generator (http://bigwww.epfl.ch/algorithms/psfgenerator/) and install them in your FIJI Plugins folder.

2. Batch process z-stacks.  To process raw data in preparation for image segmentation, you will utilize 4 custom FIJI macros found in the directory: code/FIJI/3D_Morpho_macros. This script assumes your data is an .nd2 file, but you can adjust the macro to match your file format type as needed.

Run ND2-Split-BS.ijm [./code/FIJIcode/FIJI/3D_morpho_macros/ND2-Split-BS-v5.ijm] This FIJI macro will import your raw data, split the channels into 3 TIF z-stack directories (C1, C2 and C3) inside /TIF_Output, perform rolling ball background subtraction (default value = 300) on your fluorescence data, and save those z-stacks in new directories (C2 and C3) inside the directory, /BGSub_Output. For the demo, you can run the macro two times to process the images in ./data/C_reinhardtii and ./data/C_smithii.

## Batch deconvolution

3. Deconvolve your background subtracted z-stacks. If you are processing the demo data, you can utilize the two PSF files computed in PSF Generator that we have generated based on our image acquisition parameters for the demo data. Please refer to the PSF Generator plug-in documentation (http://bigwww.epfl.ch/algorithms/psfgenerator/) if you need to generate your own PSF file for deconvolution.

Run DeconLab2-batch.ijm (./code/FIJI/3D_Morpho_macros/DeconLab2-batch.ijm) for each channel of background subtracted data. This FIJI macro will ask you for input and output directories as well as the corresponding PSF file. For the demo, you should use PSF_BW-640.tif for the cholorplast data (./BGSub_Output/C2) and PSF_BW-561.tif for the mitochondria data (./BGSub_Output/C3). The two PSF files are in ./data/demo_PSFs.

For the demo, we are using the RIF algorithm in DeconvolutionLab2 as we found that it performed best given the different deconvolution algorithms available in the plug-in. For your own data, we recommend running DecovolutionLab2 in FIJI and determining which algorithm functions best. You can modify the FIJI macro DeconLab2-batch.ijm by adjusting "RIF 0.1000" in line 30:

        algorithm = " -algorithm RIF 0.1000";

You should now have two new directories (we setup directories ./decon560 and ./decon640 when running the macro) the contain the results of deconvolution of the demo data. If you want to compare the two species at the end of the demo, make sure to process the images from both species' demo data (./data/C_reinhardtii and ./data/C_smithii).

## Generate composite images and maximum projections (MIPs) of the deconvolved data

4. The following section is not necessary for image segmentation and analysis, but if you would like to batch process your deconvolved data to view composite (multi-color) images and generate maximum intensity projections of the data you can run the following two custom FIJI macros.

Run Batch_Merge_2-channel.ijm (code/FIJI/3D_Morpho_macros/Batch_Merge_2-channel.ijm) and select each directory of deconvolved images you processed above. By default, the first channel you select will be labeled with a green LUT and the second channel with a magenta LUT. You can adjust these in the macro in line 38 by replacing "c2=" and "c6=" with other channels.

        run("Merge Channels...", "c2=" + image1 + " c6=" + image2 + " create keep");

In FIJI there are 7 options for composite channel LUTs:
        C1(red)
        C2(green)
        C3(blue)
        C4(gray)
        C5(cyan)
        C6(magenta)
        c7(yellow)

Run ZProj-contrast.ijm (code/FIJI/3D_Morpho_macros/ZProj-contrast.ijm) and select the directory where you saved your composite images generated in the previous step. This macro will perform default contrast enhancement (adjusted in lines 35 and 42 of the macro) for each channel:

        run("Enhance Contrast", "saturated=0.35");

The macro will then generate a MIP saved in a ./MIPs directory inside the selected directory of composite images.

## Image segmentation

This section of the pipeline will utilize the Allen Institute's cell segmentation software (https://www.allencell.org/segmenter.html) to generate segmentation masks of the deconvolved data you processed above. You can use the Napari plug-in or run their code through jupyter notebooks. Please refer to the documentation associated with their github repository (https://github.com/AllenCell/aics-segmentation) in order to install their software in your operating system. The napari version is accessible here: (https://www.napari-hub.org/plugins/napari-allencell-segmenter). For the purpose of this demo, we will assume you will be running your analysis in the Napari plug-in:

### Adjusting parameters for image segmentation in Napari using the Allen Institute Cell Segmentation Napari plug-in

5. Installation of Napari and the Allen Institute Cell Segmentation plug-in.

Generate a conda environment following the appropriate installation instructions specific for your operating system from the Napari documentation: https://napari.org/stable/tutorials/fundamentals/installation.html#installation

We generated an environment named

        napari-aics

and the dependencies required to run the analyses in Napari in this environment are available in this file:

        envs/napari-aics.yml

Activate your environment:

        conda activate napari-aics

And open Napari:

        napari

In Napari open up an image from the demo data (./data/C_reinhardtii). You can drag and drop the file into Napari or use File --> Open File(s) to open the image. Next, you can open up the AICS plugin by navigating to: Plugins-->napari-allencell-segmenter-->Workflow editor

You can work through the Workflow Editor to create a segmentation mask. This will allow you to see the results of each step in the workflow as well as save your own .json file to run all of your images in batch processing. We used the following inputs:

### Batch processing to generate image segmentation masks in Napari

6. Once you have generated a workflow and saved the associated .json file you are ready to batch process your data. We have provided the .json files that we generated using the Workflow editor located here: code/Napari/Chloro.json and code/Napari/Mito.json.

To batch process your images in Napari, open the napari-allencell-segmenter-->Batch processing plugin and follow the instructions, providing the directory of the data you would like to process and the location of the workflow .json file.


## Quantification

7. Now that you have generated a set of image segmentation masks based on the deconvolution of the raw data files, you are ready to quantify the data.

You will need to generate a conda environment to run two python scripts to estimate the total volume of individual algal cells based on the mitochondrial dye segmentation mask you generated in Napari and to compute the total volume of the chloroplast and mitochondrial networks in each of the images.

We generated an environment named

        volume

and the dependencies required to run the analyses in Napari in this environment are available in this file:

        envs/volume.yml

Activate your environment:

        conda activate volume

To estimate the volume as an ellipse, we wrote a script

        /code/python/ellipsoid_measure_v2.py

the processes a directory of 3D image files to compute the maximum dimensions of the largest segmented region
in each image. The maximum depth, height, and width of these regions are calculated and saved to a specified CSV file.
The script is run from the command line, accepting inputs for the directory of image files, and the path to the output CSV file.

Usage:

        python ellipse_measure_v2.py --input-dir <path_to_input_directory> --output-csv <path_to_output_csv_file>

Next, you can calculate the voxel volume of your data as well as the integrated density by providing the following script:

        /code/python/volume_v6.py

This script processes a directory of 3D image masks and a separate directory of raw data images
to compute the volume, integrated density, and mean intensity of segmented structures in the masks,
outputting these metrics to a specified output directory.
The script is run from the command line, accepting inputs for the directory of mask image files,
the directory of raw data images, and the path to the output directory.
Usage:

        python script.py --mask-dir <path_to_mask_directory> --raw-data-dir <path_to_raw_data_directory> --output-dir <path_to_output_directory>

You will need to point the script to the directory containing the segmentations masks and the directory containing the original raw data that you have split by channel using our ImageJ macro:

        ND2-Split-BS-v5.ijm


## Statistics and Generating Plots

This set of R notebooks takes the output of the dimension measurements generated using the Python code in this GitHub (/code/python/ellipsoid_measure.py and /code/python/volume.py) and calculates the volume of an ellipsoid and the eccentricity as estimates of the cell-body morphology. We then combined those calculated measurements with the organelle dimensions into a csv file ("output_cell_volume_mito_chlor.csv") and filtered the data, checked summary statistics, made violin plots of the data, and compared each measurement by species using non-parametric statistics.

# Versions and platforms
*Fiji macro* was used with ImageJ2 Version 2.14.0/1.54f

*R* code was run with R version 4.3.0 (2023-04-21)

*R Libraries/packages*: tidyverse 2.0.0, dplyr     1.1.2, readr     2.1.4, forcats   1.0.0, stringr   1.5.0, ggplot2   3.4.2, tibble    3.2.1, lubridate 1.9.2, tidyr     1.3.0, purrr     1.0.1

*Python* code was run with Python 3.11.5

Computation was performed on MacBook Pro computers with the following specifications:

macOS: Ventura 13.4.1 (c)
Chip Apple M2 Max
Memory 32 Gb

3D morphology:

macOS: Ventura 13.5.1 (c)
Chip Apple M1 Max
Memory 64Gb
# Feedback, contributions, and reuse

We try to be as open as possible with our work and make all of our code both available and usable.
We love receiving feedback at any level, through comments on our pubs or Twitter and issues or pull requests here on GitHub.
In turn, we routinely provide public feedback on other people’s work by [commenting on preprints](https://sciety.org/lists/f8459240-f79c-4bb2-bb55-b43eae25e4f6), filing issues on repositories when we encounter bugs, and contributing to open-source projects through pull requests and code review.

Anyone is welcome to contribute to our code.
When we publish new versions of pubs, we include a link to the "Contributions" page for the relevant GitHub repo in the Acknowledgements/Contributors section.
If someone’s contribution has a substantial impact on our scientific direction, the biological result of a project, or the functionality of our code, the pub’s point person may add that person as a formal contributor to the pub with "Critical Feedback" specified as their role.

Our policy is that external contributors cannot be byline-level authors on pubs, simply because we need to ensure that our byline authors are accountable for the quality and integrity of our work, and we must be able to enforce quick turnaround times for internal pub review.
We apply this same policy to feedback on the text and other non-code content in pubs.

If you make a substantial contribution, you are welcome to publish it or use it in your own work (in accordance with the license — our pubs are CC BY 4.0 and our code is openly licensed).
We encourage anyone to build upon our efforts.
