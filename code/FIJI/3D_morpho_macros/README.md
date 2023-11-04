This directory contains 4 FIJI macros to process multiple images in a directory.
ND2-Split-BS-v5.ijm will convert .nd2 files from Nikon Elements, split the images into their separate channels (in this case, brightfield = C1, 640 or chloroplast auto-fluorescence is C2, and 561 or mitochondrial dye staining is C3). These files will be located in new directories ./TIF_Output/C1 C2 and C3 The macro also performs rolling ball subtraction with a user input (we used a value of 300) and saves the C2 and C3 data in new directories as ./BGSub_Output/C2 and C3.

DeconLab2-batch_v4.ijm allows for batch processing of .tif z-stacks using the DeconvolutionLab2 plug-in in FIJI.

Batch_Merge_2-channel_v2.ijm allows you to batch process the deconvoluted data and visualize the results as a composite image

ZProj-contrast-v2.ijm allows you to batch process composite images to generate maximum intensity projections (MIPs)
