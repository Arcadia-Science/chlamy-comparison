/*
 * Macro opens image stacks, 
 * allows user to select square regions of interest, duplicates regions, 
 * saves stacks as tif files. Processes multiple images in a folder.
 */

// Choose "experiments" directory with raw data of cells in pools
#@ File (label = "Input directory", style = "directory") input 
suffix = ".tif";

run("ROI Manager...");
run("Set Measurements...", "area mean modal min integrated redirect=None decimal=3");

// Define function to scan folders/subfolders/files to find files with correct suffix
function processFolder(in) {
    list = getFileList(in);
    list = Array.sort(list);
    for (i = 0; i < list.length; i++) {
        if(File.isDirectory(in + File.separator + list[i])){
            
            // If it is a directory, process it
            processFolder(in + File.separator + list[i]);
        } else if(endsWith(list[i], suffix) && indexOf(in, "raw_sample") != -1){
   
            // Process only if the folder is named 'raw_sample
            roi_interactive_func(in + list[i]);
        }
    };
};

/* Define function that will open an image, make a square, and allow the user to define square regions of 
 * interest. After the user is finished, the function will duplicate the regions as stacks
 * and then save them as tif files. 
 */

function roi_interactive_func(file) {
	print("Processing: " + file);
	run("Bio-Formats Importer", "open=" + file + " color_mode=Default rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
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
	waitForUser("Select ROIs by moving square over the ROI and clicking 'Add' in the ROI manager");
	
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
   		
   		
   		outputdir = substring(in, 0, indexOf(in, "raw"));
   		print(outputdir);
   		if (!File.isDirectory(outputdir + "pools")){
   			File.makeDirectory(outputdir + "pools");
   		};
   		
   		if (!File.isDirectory(outputdir + "pools" + File.separator + group)){
   			File.makeDirectory(outputdir + "pools" + File.separator + group);
   		};
   		
   		//Save as .tif
   		saveAs("Tiff", outputdir + File.separator + "pools" + File.separator + group + File.separator + roi_name + ".tif");
   		close(roi_name);
	};
	
	run("Close All");
	roiManager("deselect");
	roiManager("Delete");
};	

processFolder(input);