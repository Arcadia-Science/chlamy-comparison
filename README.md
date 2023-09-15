# Phenotypic Analysis of Interfertile Algal Species

This repository contains code for image processing and analysis to compare phenotypes of interfertile *Chlamydomonas* species. These analyses are included in the publication [Phenotypic differences between interfertile Chlamydomonas species](https://doi.org/10.57844/arcadia-35f0-3e16).

![Chlamydomonas smithii is larger than C. reinhardtii but they have a similar shape](https://github.com/Arcadia-Science/chlamy-comparison/assets/110641190/a6854e63-e4f6-4779-904e-02ca65fb4d4d)

Release v2.1

Github

[![DOI](https://zenodo.org/badge/644048016.svg)](https://zenodo.org/badge/latestdoi/644048016)

Data Repository

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8326749.svg)](https://doi.org/10.5281/zenodo.8326749)

# Computational Protocols

For each step run the commands indicated in code blocks from the "chlamy-comparison" directory.

## Protocol for segmenting cells and taking measurements of 2D morphology


1. Download data from Zenodo. This will be a directory called "experiments" with subdirectories and image data.

        curl -JLO https://zenodo.org/record/8326749/files/experiments.zip?download=1

2. Crop "pools" of swimming cells from raw videos using the Fiji Macro batch_interactive_crop_savetif.v.0.0. Samples of raw videos are contained in the the "experiments/{experiment}/raw_sample" directories. Choose "experiments" as the input directory. [Link to Fiji macro](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/FIJI/batch_interactive_crop_savetif.ijm)

3. Parse focal sequences of frames from "pools". [Link Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/focus_varLaplacv.0.1.py)

        python3 code/python/focus_varLaplacv.0.1.py

4. Sample the focal sequences randomly to generate a training set for pixel classification. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/sample_training_set.v.1.0.py)

        python3 code/python/sample_training_set.v.1.0.py


5. Perform pixel classification with Ilastik. Load the training sets and process the focal sequences in batch. Directory = main/experiments/ilastik

6. Organize probability maps by species and pool ID. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/organize_tif_sp_pool.v.2.0.py)

        python3 code/python/organize_tif_sp_pool.v.2.0.py

7. **Python**: Segment cells and take 2D morphology measurements. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/segment_chlamy.v.2.1.py)

        python3 code/python/segment_chlamy.v.2.1.py

   **Cellprofiler**: Alternatively, segment the cells and take measurements in Cellprofiler with the pipeline chlamy_segment.cppipe. [Link to Cellprofiler pipeline](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/Cellprofiler/chlamy_segment.cppipe)

8.  Identify the maximal area measurement per focal sequence. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/max_area_focus_seq.v.0.4.py)

        python3 code/python/max_area_focus_seq.v.0.4.py

9.  Parse per pool mean measurements. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/parse_2d_morphology_exp_species.v.0.0.py)

        python3 code/python/parse_2d_morphology_exp_species.v.0.0.py

## Script for generating vector graphics of idealized cell


    python3 code/python/chlamy_modeler.py

## Protocol for visual and qualitative assessments of cell morphology

1. Creat a list of images with maximum area objects with relevant metadata. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/max_area_image_obj_list.v.0.1.py)

        python3 code/python/max_area_image_obj_list.v.0.1.py

2. Identify image frames to calculate swim angle. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/frames_for_angle.v.0.0.py)

        python3 code/python/frames_for_angle.v.0.0.py

3. Calculate swim angle and swim angle relative to the Y-axis. Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/swim_angle.v.0.2.py)

       python3 code/python/swim_angle.v.0.2.py

4. Mask cells. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/image_mask.v.0.0.py)

       python3 code/python/image_mask.v.0.0.py

5. Get statistics about the objects. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/object_stats.v.0.0.py)

       python3 code/python/object_stats.v.0.0.py

6. Crop and reorient cells so they are swimming "up" and the major axis of the cell is aligned with the y-axis. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/crop_orient_major_regionprops.v.0.2.py)

        python3 code/python/crop_orient_major_regionprops.v.0.2.py

7. Combine cells into stacks by experiment and species. [Link to Python script](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/python/save_stack.v.0.3.py)

        python3 code/python/save_stack.v.0.3.py

8.  Create a substack with the number of frames you want in the final video in Fiji.

9.  Calculate cumulative average projections from the substacks with the Fiji macro batch_sequential_avg_proj.v.0.0.ijm. [Link to Fiji macro](https://github.com/Arcadia-Science/chlamy-comparison-private/blob/main/code/FIJI/batch_sequential_avg_proj.v.0.0.ijm)


# Versions and platforms
*Fiji macro* was used with ImageJ2 Version 2.14.0/1.54f

*R* code was run with R version 4.3.0 (2023-04-21)

*R Libraries/packages*: tidyverse 2.0.0, dplyr     1.1.2, readr     2.1.4, forcats   1.0.0, stringr   1.5.0, ggplot2   3.4.2, tibble    3.2.1, lubridate 1.9.2, tidyr     1.3.0, purrr     1.0.1

*Python* code was run with Python 3.11.5

Computation was performed on MacBook Pro computer with the following specifications:

macOS: Ventura 13.4.1 (c)
Chip Apple M2 Max
Memory 32 Gb

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
