/*
 * Macro to perform cumulative standard deviation projections, also known as tracks.
 * This Fiji macro scans a directory for TIFF files with a specified suffix,
 * then opens each file as a Bio-Formats movie,
 * applies image processing to generate standard deviation images for each frame of the input movie,
 * and saves the standard deviation images in a separate directory within the specified output directory.
 */

// Prompt user to select the input directory
#@ File (label = "Input directory", style = "directory") input

// Prompt user to select the output directory
#@ File (label = "Output directory", style = "directory") output

// Prompt user to specify the file suffix
#@ String (label = "File suffix", value = ".tif") suffix

// Call the processFolder function to scan the input directory and process TIFF files with the specified suffix
processFolder(input);

// Define a function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {

	// Get a list of files in the input directory
	list = getFileList(input);

	// Sort the list of files alphabetically
	list = Array.sort(list);

	// Loop through each file in the list
	for (i = 0; i < list.length; i++) {

		// If the file ends with the specified suffix
		if(endsWith(list[i], suffix))

			// Call the processFile function to open and process the current TIFF file
			processFile(input, output, list[i]);
	};
};

// Define a function to process a single TIFF file
function processFile(input, output, file) {

	// Print the name of the current file to the console
	print("Processing: " + input + File.separator + file);

	// Open the TIFF file as a Bio-Formats movie
	run("Bio-Formats Importer", "open=" + input + File.separator + file + " color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");

	// Get the title of the current image stack
	imageTitle = getTitle();
	print(imageTitle);

	// Rename the current image stack to "stack"
	stack = getImageID();
	rename("stack");

	// Get the dimensions of the current image stack
	getDimensions(width, height, channels, slices, frames);

	// Get the base name of the current file (without the suffix)
	baseNameEnd = indexOf(imageTitle, ".tif");
	baseName = substring(imageTitle, 0, baseNameEnd);
	rename("stack");

	// Loop through each frame of the current image stack
	for (f = 2; f <= frames; f++){

		// Select the current frame of the image stack
		selectWindow("stack");

		// Apply the "Z Project..." command to the current frame of the image stack, projecting the standard deviation in the Z dimension
		run("Z Project...", "stop=" + f + " projection=[Average Intensity]");
		
		run("Enhance Contrast", "saturated=0.35");

		// Save the output standard deviation image to the VAR directory within the output directory
		saveAs("Tiff", output + File.separator + baseName + "_std_f" + f + ".tif");
		rename("STD");

		// Close the output standard deviation image
		close("STD");
	};
	close("stack");
	// Close all windows
	//run("Close All");
};

// Get the end time of the macro
endtime = getTime();

// Print the end time to the console
print("End time: " + endtime);
