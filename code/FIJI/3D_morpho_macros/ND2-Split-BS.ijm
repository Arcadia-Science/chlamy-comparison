function checkAndMakeDir(directoryPath) {
    if (!File.exists(directoryPath)) {
        File.makeDirectory(directoryPath);
        if (!File.exists(directoryPath)) {
            showMessage("Error", "Failed to create directory: " + directoryPath);
            exit();
        }
    }
}

// Create a custom dialog for Image Directory selection
Dialog.create("Select Folder for of .nd2 images you would like to convert");
Dialog.addMessage("This macro requires you to have .nd2 image files with three channels. Please select the folder of .nd2 images you would like to convert to TIF files");
Dialog.show();

// Prompt user to select a directory
inputDirectory = getDirectory("Choose a Directory of ND2 Images...");
// Prompt user to input a value for rolling ball substraction
rollingBallRadius = getNumber("Enter rolling ball radius for background subtraction:", 300); // 300 is the default value

// Define output directories (add or remove additional channels below as needed based on your image acquisition settings)
tifDirectory = inputDirectory + "TIF_Output/";
bgSubDirectory = inputDirectory + "BGSub_Output/";
tifDirectoryC1 = inputDirectory + "TIF_Output/C1/";
tifDirectoryC2 = inputDirectory + "TIF_Output/C2/";
tifDirectoryC3 = inputDirectory + "TIF_Output/C3/";
bgSubDirectoryC2 = inputDirectory + "BGSub_Output/C2/";
bgSubDirectoryC3 = inputDirectory + "BGSub_Output/C3/";

// Create output directories if they don't exist
File.makeDirectory(tifDirectory);
File.makeDirectory(bgSubDirectory);
File.makeDirectory(tifDirectoryC1);
File.makeDirectory(tifDirectoryC2);
File.makeDirectory(tifDirectoryC3);
File.makeDirectory(bgSubDirectoryC2);
File.makeDirectory(bgSubDirectoryC3);

// Get list of files in the directory
fileList = getFileList(inputDirectory);

// Loop through all files
for (i = 0; i < fileList.length; i++) {
    fullPath = inputDirectory + fileList[i];

    // Ensure the file is an .nd2 image
    if (fileList[i].endsWith(".nd2")) {
        
        // Use the Bio-Formats Importer with a predefined configuration file
        run("Bio-Formats Importer", "open=[" + fullPath + "] autoscale color_mode=Grayscale rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT");

        // Adjust the base title for the naming convention
        baseTitle = fileList[i].substring(0, fileList[i].lastIndexOf('.nd2'));

		// Process and save Channel 1
        selectWindow(baseTitle + ".nd2 - C=0"); // This corresponds to Channel 1
        saveAs("Tiff", tifDirectoryC1 + baseTitle + "_C1.tif");
        
        // Process and save Channel 2
        selectWindow(baseTitle + ".nd2 - C=1"); // This corresponds to Channel 2
        saveAs("Tiff", tifDirectoryC2 + baseTitle + "_C2.tif");
        run("Subtract Background...", "rolling=" + rollingBallRadius + " stack");
        saveAs("Tiff", bgSubDirectoryC2 + baseTitle + "_C2_BGSub.tif");
        close();

        // Process and save Channel 3
        selectWindow(baseTitle + ".nd2 - C=2"); // This corresponds to Channel 3
        saveAs("Tiff", tifDirectoryC3 + baseTitle + "_C3.tif");
        run("Subtract Background...", "rolling=300 stack");
        saveAs("Tiff", bgSubDirectoryC3 + baseTitle + "_C3_BGSub.tif");
        close();
    }
}

run("Close All");

// Inform the user that processing is complete
showMessage("Processing Complete", "All ND2 images have been processed and saved!");
