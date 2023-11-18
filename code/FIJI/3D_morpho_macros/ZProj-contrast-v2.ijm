// Create a custom dialog for Image Directory selection
Dialog.create("Select Directory of composite images");
Dialog.addMessage("Please select the folder of composite images you would like to process");
Dialog.show();

// Get directory
dir = getDirectory("Select a Directory of Composite Images");

// Define save directory
saveDir = dir + "MIPs" + File.separator;

// Create save directory if they don't exist
File.makeDirectory(saveDir);

// Get list of files in the directory
list = getFileList(dir);

setBatchMode(true); // Start batch mode

for (i = 0; i < list.length; i++) {
    if (endsWith(list[i], ".tif")) {
        open(dir + list[i]);
        title = getTitle();
    
        // Z-project (max intensity)
        run("Z Project...", "projection=[Max Intensity]");
        mipTitle = "MAX_" + title;
        close(title); // Close the original image to save memory

        // Split channels
        run("Split Channels");
        close(mipTitle); // Close the MIP image to save memory

        // Enhance contrast for channel 1
        ch1Title = "C1-" + mipTitle;
        if (isOpen(ch1Title)) {
            selectWindow(ch1Title);
            run("Enhance Contrast", "saturated=0.35");
        }

        // Enhance contrast for channel 2
        ch2Title = "C2-" + mipTitle;
        if (isOpen(ch2Title)) {
            selectWindow(ch2Title);
            run("Enhance Contrast", "saturated=0.35");
        }

        // Name for the merged image
        mergedTitle = "Merged_" + mipTitle;

        // Merge channels back
        run("Merge Channels...", "c2=" + ch1Title + " c6=" + ch2Title);
        close(ch1Title); // Close ch1 image to save memory
        close(ch2Title); // Close ch2 image to save memory

        // Check if the merged image titled "RGB" is open
        if (isOpen("RGB")) {
            // Rename to a custom title
            rename(mergedTitle);
            
            // Save the merged image with the determined title
            saveAs("Tiff", saveDir + mergedTitle);

            // Close the merged image
            close();
        } else {
            print("Failed to merge: " + title);
        }
    }
}

setBatchMode(false); // End batch mode

print("Processing complete!");
