// Create a custom dialog for Image Directory selection
Dialog.create("Select Folder for Channel 1 images");
Dialog.addMessage("Please select the folder of images from the first channel you would like to merge");
Dialog.show();

macro "Batch Merge Swapped Names with Saving" {
    dir1 = getDirectory("Select Folder for Channel 1");

// Create a custom dialog for Image Directory selection
Dialog.create("Select Folder for Channel 2 images");
Dialog.addMessage("Please select the folder of images from the second channel you would like to merge");
Dialog.show();

    dir2 = getDirectory("_Select Folder for Channel 2");
    
// Create a custom dialog for Image Directory selection
Dialog.create("Select Folder to save processed imaged");
Dialog.addMessage("Please select the destination folder for merged imaged");
Dialog.show();

    saveDir = getDirectory("Select Directory to Save Merged Images"); // Choose where to save the merged images
    list = getFileList(dir1); 

    for (i=0; i<list.length; i++) {
        mergedTitle = "Merged_" + list[i];

        // Open image from the first directory (which has C3 names)
        open(dir1 + list[i]);
        image1 = getTitle();
        
        // Convert the name for the second directory (swap C3 to C2)
        imageName2 = replace(list[i], "C3_BGSub.tif", "C2_BGSub.tif");
        
        open(dir2 + imageName2);
        image2 = getTitle();

        // Merge channels
        run("Merge Channels...", "c2=" + image1 + " c6=" + image2 + " create keep");

        // Close opened source images
        selectWindow(image1);
        close();
        
        selectWindow(image2);
        close();

        // Save the merged composite image
        selectWindow("Composite");
        saveAs("Tiff", saveDir + mergedTitle);
        close();
    }
}

Batch Merge Swapped Names with Saving();
