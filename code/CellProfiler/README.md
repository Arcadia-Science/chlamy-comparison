The Cellprofiler pipeline chlamy_segment.cppipe takes probability maps that were the outputs of an Ilastik pixel classfication. The output is the segmented cells as objects in images. Foreground was defined as pixels with >= 50% probability of a chlamydomonas cell. A size cutoff was implemented so only objects between 5 and 40 pixels in diameter were considered objects.

The Cellprofiiler pipeline CW_Pipeline.cppipe segments individual cells from raw greyscale .tif files. A size cutoff was implemented so only objects between 30 and 100 pixels in diameter were considered objects. Object Intensity and Object Size/Shape were measured, and data was exported to a spreadsheet. 

The Cellprofiler pipeline CW_Pipeline_Extracted.cppipe follows the same pipeline as above but exports the data as an SQLite database. In most cases, the number of files going through this pipeline will be much larger after single cell extraction. This will prevent exporting to spreadsheets. 
