/*
 * Macro opens image stacks, 
 * allows user to select square regions of interest, duplicates regions, 
 * saves stacks as tif files. Processes multiple images in a folder.
 */

#@ File (label = "Input directory", style = "directory") input
#@ File (label = "Output directory", style = "directory") output
#@ String (label = "File suffix", value = ".nd2") suffix

//Time in milliseconds
start = getTime();
run("ROI Manager...");
run("Set Measurements...", "area mean modal min integrated redirect=None decimal=3");

// Define function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(endsWith(list[i], suffix))
			roi_interactive_func(input, output, list[i]);
	};
};

/* Define function that will open an image, make a square, and allow the user to define square regions of 
 * interest. After the user is finished, the function will duplicate the regions as stacks
 * and then save them as tif files. 
 */

function roi_interactive_func(input, output, file) {
	print("Processing: " + input + File.separator + file);
	run("Bio-Formats Importer", "open=" + input + File.separator + file + " color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
	imgName = getTitle();
	print(imgName);
	
	//Define baseName, name without file type
	baseNameEnd=indexOf(imgName, suffix);
	baseName=substring(imgName, 0, baseNameEnd);
	
	//Define species
	groupbegin=indexOf(imgName, "_w");
	group= substring(imgName, 0, 2);
	
	run("ROI Manager...");
	makeRectangle(0, 0, 182, 182);
	waitForUser("Select ROIs");
	
	//Process each ROI
	n = roiManager("count");
	for (x = 0; x < n; x++) {
		selectImage(imgName);
   		roiManager("select", x);
   		
   		//Duplicate each roi
   		run("Duplicate...", "duplicate");
   		roi_name = baseName + "_" + x;
   		print(roi_name);
   		rename(roi_name);
   		selectImage(roi_name);
   		
   		//Save as .tif
   		saveAs("Tiff", output + File.separator + roi_name + ".tif");
   		close(roi_name);
	};
	
	run("Close All");
	roiManager("deselect");
	roiManager("Delete");
};	

processFolder(input);