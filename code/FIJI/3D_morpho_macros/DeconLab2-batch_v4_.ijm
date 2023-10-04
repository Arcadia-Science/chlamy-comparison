// Activate batch mode for better performance
setBatchMode(true);

// Create a custom dialog for Image Directory selection
Dialog.create("Image Selection");
Dialog.addMessage("Please select the Directory of images you would like to use to run Deconvolution Lab2.");
Dialog.show();

inputDir = getDirectory("Choose a Directory of Images...");

// Create a custom dialog for Image Directory selection
Dialog.create("Proceed Image Directory Selection");
Dialog.addMessage("Please select the Directory where you would like the processed images to reside in.");
Dialog.show();

outputDir = getDirectory("_Choose an Output Directory...");

fileList = getFileList(inputDir);

// Create a custom dialog for PSF selection
Dialog.create("PSF Selection");
Dialog.addMessage("Please select the PSF image file.");
Dialog.show();

// Prompt user to select the PSF image file
psfFilePath = File.openDialog("Select PSF image file");
if (psfFilePath == "") {
    // Deactivate batch mode before showing message and exiting
    setBatchMode(false);
    exit("PSF image selection canceled.");
}

// Pre-defined settings
psf = " -psf file " + psfFilePath;
algorithm = " -algorithm RIF 0.1000";
outputPath = " -path " + outputDir;  // Adjusted to the chosen output directory

for (i = 0; i < fileList.length; i++) {
    if (endsWith(fileList[i], ".tif")) {
        
        open(inputDir + fileList[i]);  // Open the target image
        
        image = " -image platform active";  // Reference the currently active image

        commandOptions = image + psf + algorithm + outputPath;  // Construct the command options

        run("DeconvolutionLab2 Run", commandOptions);  // Run DeconvolutionLab2 with the parameters

        wait(15000);  // Wait for DeconvolutionLab2 to finish processing

        // Save the result ("Final Display of RIF")
        processedFileName = "processed_" + fileList[i];
        if (isOpen("Final Display of RIF")) {
            selectWindow("Final Display of RIF");
            saveAs("Tiff", outputDir + processedFileName);
            close();
        }

        // Close the original image
        if (isOpen(fileList[i])) {
            selectWindow(fileList[i]);
            close();
        }
    }
}

// Deactivate batch mode once processing is complete
setBatchMode(false);
