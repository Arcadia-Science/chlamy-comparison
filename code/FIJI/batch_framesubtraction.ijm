/*
 * Macro to open image stacks, perform standard deviation projections, split channels, perform frame subtraction, and save images.
 */

#@ File (label = "Input directory", style = "directory") input
#@ File (label = "Output directory", style = "directory") output
#@ String (label = "File suffix", value = ".nd2") suffix


processFolder(input);

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + File.separator + list[i]))
			File.makeDirectory(output + File.separator + list[i]);
			File.makeDirectory(output + File.separator + list[i] + File.separator + "STD");
			File.makeDirectory(output + File.separator + list[i] + File.separator + "subtract");
			File.makeDirectory(output + File.separator + list[i] + File.separator + "frames");
			processFolder(input + File.separator + list[i]);
		if(endsWith(list[i], suffix))
			//File.makeDirectory(output + File.separator + list[i]);
			processFile(input, output, list[i]);
	}
}

function processFile(input, output, file) {
	print("Processing: " + input + file);
	//opens nd2 movie
	run("Bio-Formats Importer", "open=" + input + file + " color_mode=Default rois_import=[ROI manager] view=Hyperstack 			stack_order=XYCZT");
	imageTitle = getTitle();
	stack = getImageID();
	//Scale by 0.5
	run("Scale...", "x=0.5 y=0.5 z=1.0 width=1152 height=1152 depth=399 interpolation=Bicubic average process create");
	rename("stack");
	close(imageTitle);
	getDimensions(width, height, channels, slices, frames);
	filepath = File.getParent(input + file);
	baseNameBegin=indexOf(filepath, "raw");
	newfolder=substring(filepath, baseNameBegin + 4);
	//Z project the standard deviation to look at swimming tracks
	run("Z Project...", "projection=[Standard Deviation]");
	selectWindow("STD_stack");
	run("8-bit");
	saveAs("Tiff", output + "/" + newfolder + "/STD/" + file + "_STD.tif");
	close();
	for (t=12; t<=frames; t++) {
		selectWindow("stack");
		//define frame number with three digits
		if (t<10){
			frameinc = "_#00" + t;
		};
		if (t>9 && t<100){
			frameinc = "_#0" + t;
		};
		if (t>99){
			frameinc = "_#" + t;
		};
		if(!File.exists(output + "/" + newfolder + "/subtract/" + file + frameinc + ".tif")){
			run("Make Substack...", "  slices=" + t);
			image2 = getImageID();
			rename("second");
			
			selectImage("stack");
			tosub = t - 11;
			run("Make Substack...", "  slices=" + tosub);
			image1 = getImageID();
			rename("first");
			//subtract frame 1 from frame 12
			imageCalculator("Subtract create", "second", "first");
			subtracted = getImageID();
			rename("sub");
			selectWindow("sub");
			run("8-bit");
			print("saving to..." + output + "/" + newfolder + "/subtract/" + file + frameinc + ".tif");
			saveAs("Tiff", output + "/" + newfolder + "/subtract/" + file + frameinc + ".tif");
			close("first");
			close("sub");
			selectWindow("second");
			run("8-bit");
			saveAs("Tiff", output + "/" + newfolder + "/frames/" + file + frameinc + ".tif");
			close("second");
		};
	};
	run("Close All");
}
