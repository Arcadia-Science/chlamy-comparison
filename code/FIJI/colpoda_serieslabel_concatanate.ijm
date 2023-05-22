dir=getDirectory("Choose a Directory");
print(dir);
//splitDir=dir + "Concat";
//print(splitDir);
//File.makeDirectory(splitDir);
list = getFileList(dir);

for (i=0; i<list.length; i++) {
     if (endsWith(list[i], ".tif")){
     	print(i + ": " + dir+list[i]);
        open(dir+list[i]);
        imgName=getTitle();
        baseNameEnd=indexOf(imgName, ".tif");
        baseName=substring(imgName, 0, baseNameEnd);
       	run("Series Labeler", "font=SansSerif style=Plain just=Left color=White bkgd=None size=50 angle=0 antialiased stack_type=[time series or movie] label_format=[Custom Format] custom_suffix=h custom_format=[] label_unit=[Custom Suffix] decimal_places=0 startup=" + i*8 + " interval=0.00000083 every_n-th=1 first=1 last=50 location_presets=Custom x_=1900 y_=0");
		run("Series Labeler", "font=SansSerif style=Plain just=Left color=White bkgd=None size=50 angle=0 antialiased stack_type=[time series or movie] label_format=[Custom Format] custom_suffix=sec custom_format=[] label_unit=[Custom Suffix] decimal_places=1 startup=0.000000000 interval=0.083 every_n-th=1 first=1 last=50 location_presets=[Upper Right]");
        run("Scale Bar...", "width=100 height=12 font=64 color=White background=None location=[Lower Right] overlay label");
        saveAs("Tiff", dir + baseName + "concat.tif");
        
     }
}
