The R notebook [parse_objects.ipynb](./parse_objects.ipynb) in this directory uses a directory and subdirectories with CSV files of 2-dimensional algal cell morphology measurements from Cellprofiler.
This CSV file is available on zenodo at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8165714.svg)](https://doi.org/10.5281/zenodo.8165714)

It can be downloaded using the following command:

```
curl -JLO https://zenodo.org/record/8165714/files/experiments_csv.zip\?download\=1
```

The [motility_v3_pub.ipynb](./motility_v3_pub.ipynb) notebook relies on the two csv files in the [data](./data) directory fseq_measurements.v.1.csv and fseq_velocities_well_avg_2.csv.

The [autocorrelation_and_joint_velocity_distribution_analyses.ipynb](./autocorrelation_and_joint_velocity_distribution_analyses.ipynb) relies on a .RDS file of cell trajectories available in the [data](./data) directory named chlamydomonas_species_full_motility_trajectories.RDS.

The [ellipsoid_volume_v4.ipynb](./ellipsoid_volume_v4.ipynb) notebook relies on one of the csv files in the [data](./data) directory and calculates the cell volume and eccentricity values for each stack of images.

The [organelle_ratio_v4.ipynb](./organelle_ratio_v4.ipynb) notebook relies on one of the csv files in the [data](./data) directory and calculates the mitochondria and chloroplast volumes, tests normality of the data, compares the measurements for each species and generates violin plots.
