"""
This Python script collects and processes image sequences
from a nested directory structure containing various "experiments" and "species."
It randomly selects a specified number of TIFF image sequences from each category, combines them,
and saves the combined sequences in a new "training" folder within each experiment's directory.
The aim is to generate training datasets for each species in each experiment.
"""

import os
import random
import numpy as np
from skimage import io

# Number of sequences you want for training from each basename
N_TRAINING_SAMPLES = 3

# Source root folder
SOURCE_ROOT = './experiments'  # Current directory

# Extract all experiments from the source root
experiments = [folder for folder in os.listdir(SOURCE_ROOT) if os.path.isdir(os.path.join(SOURCE_ROOT, folder))]

for experiment in experiments:
    species_path = os.path.join(SOURCE_ROOT, experiment, 'focus')
    if os.path.exists(species_path):
        species_list = [folder for folder in os.listdir(species_path) if os.path.isdir(os.path.join(species_path, folder))]

        for species in species_list:
            base_name_path = os.path.join(species_path, species)
            base_names = [folder for folder in os.listdir(base_name_path) if os.path.isdir(os.path.join(base_name_path, folder))]

            # Placeholder to accumulate sequences
            combined_seqs = []

            for base_name in base_names:
                sequence_path = os.path.join(base_name_path, base_name)
                sequences = [seq for seq in os.listdir(sequence_path) if seq.endswith('.tif')]

                # Randomly select sequences for training
                training_samples = random.sample(sequences, min(N_TRAINING_SAMPLES, len(sequences)))

                # Read and accumulate sequences
                for sample in training_samples:
                    seq_data = io.imread(os.path.join(sequence_path, sample))
                    combined_seqs.append(seq_data)

            # Combine sequences and save
            combined_seqs = np.concatenate(combined_seqs, axis=0)
            dest_folder = os.path.join(SOURCE_ROOT, experiment, 'training', species)
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, f"{experiment}_training_data.tif")
            io.imsave(dest_path, combined_seqs)

print("Training samples created in each experiment's 'training' directory.")
