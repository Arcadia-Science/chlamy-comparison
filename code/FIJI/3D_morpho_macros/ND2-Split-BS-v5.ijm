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
rollingBallRadius = getNumber("Enter rolling ball radius for background subtraction:", 300); // 300 is the default value

// Define output directories
tifDirectory = inputDirectory + "TIF_Output/";
bgSubDirectory = inputDirectory + "BGSub_Output/";
tifDirectoryC1 = inputDirectory + "TIF_Output/C1/";
tifDirectoryC2 = inputDirectory + "TIF_Output/C2/";
tifDirectoryC3 = inputDirectory + "TIF_Output/C3/";
bgSubDirectoryC2 = inputDirectory + "BGSub_Output/C2/";
bgSubDirectoryC3 = inputDirectory + "BGSub_Output/C3/";

// Create output directories if they don't exist
checkAndMakeDir(tifDirectory);
checkAndMakeDir(bgSubDirectory);
checkAndMakeDir(tifDirectoryC1);
checkAndMakeDir(tifDirectoryC2);
checkAndMakeDir(tifDirectoryC3);
checkAndMakeDir(bgSubDirectoryC2);
checkAndMakeDir(bgSubDirectoryC3);

// Get list of files in the directory
fileList = getFileList(inputDirectory);

setBatchMode(true); // Start batch mode

for (i = 0; i < fileList.length; i++) {
    fullPath = inputDirectory + fileList[i];

    // Ensure the file is an .nd2 image
    if (fileList[i].endsWith(".nd2")) {
        
        run("Bio-Formats Importer", "open=[" + fullPath + "] autoscale color_mode=Grayscale rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT");

        baseTitle = fileList[i].substring(0, fileList[i].lastIndexOf('.nd2'));

        // Process and save Channel 1
        selectWindow(baseTitle + ".nd2 - C=0");
        saveAs("Tiff", tifDirectoryC1 + baseTitle + "_C1.tif");
        close();

        // Process and save Channel 2
        selectWindow(baseTitle + ".nd2 - C=1");
        saveAs("Tiff", tifDirectoryC2 + baseTitle + "_C2.tif");
        run("Subtract Background...", "rolling=" + rollingBallRadius + " stack");
        saveAs("Tiff", bgSubDirectoryC2 + baseTitle + "_C2_BGSub.tif");
        close();

        // Process and save Channel 3
        selectWindow(baseTitle + ".nd2 - C=2");
        saveAs("Tiff", tifDirectoryC3 + baseTitle + "_C3.tif");
        run("Subtract Background...", "rolling=300 stack");
        saveAs("Tiff", bgSubDirectoryC3 + baseTitle + "_C3_BGSub.tif");
        close();
    }
}

setBatchMode(false); // End batch mode

showMessage("Processing Complete", "All ND2 images have been processed and saved!");
