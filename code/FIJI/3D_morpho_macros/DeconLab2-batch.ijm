// Create a custom dialog for Image Directory selection
Dialog.create("Image Selection");
Dialog.addMessage("Please select the Directory of images you would like to use to run Deconvolution Lab2.");
Dialog.show();

inputDir = getDirectory("Choose a Directory of Images...");

// Create a custom dialog for Image Directory selection
Dialog.create("Proceed Image Directory Selection");
Dialog.addMessage("Please select the Directory where you would like to processed images to reside in.");
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
    exit("PSF image selection canceled.");
}

// Pre-defined settings
psf = " -psf file " + psfFilePath;
algorithm = " -algorithm RIF 0.1000";
outputPath = " -path " + outputDir;  // Adjusted to the chosen output directory

for (i = 0; i < fileList.length; i++) {
    if (endsWith(fileList[i], ".tif")) {
        
        // Open the target image
        open(inputDir + fileList[i]);
        
        // Reference the currently active image (which is the one we just opened)
        image = " -image platform active";

        // Construct the command options
        commandOptions = image + psf + algorithm + outputPath;

        // Run DeconvolutionLab2 with the parameters
        run("DeconvolutionLab2 Run", commandOptions);

        // Wait for DeconvolutionLab2 to finish processing (10-second delay as an example)
        wait(10000); 

        // Save the result ("Final Display of RIF")
        processedFileName = "processed_" + fileList[i];
        if (isOpen("Final Display of RIF")) {
            selectWindow("Final Display of RIF");
            saveAs("Tiff", outputDir + processedFileName);
            close();
        }

        // Close the original image
        close();
    }
}
