library(MASS)

#Function to load chlamy motility data
load_chlamy_motility = function(directory,
                                experiment_length_cutoff = 200){
  
  #Get names of directories
  n = list.files(directory)
  
  objs = list()
  
  #Loop through directories and load
  for(j in 1:length(n)){
    
    #Create empty list to save cell object data into
    cells = list.files(paste(directory, n[j], sep = ''))
    
    #Loop and load
    for(k in 1:length(cells)){
      
      #Get unique ID for each cell
      name = paste(directory, n[j], cells[k], sep = '-')
      
      #Load
      tmp = read.csv(paste(directory, n[j], '/', cells[k], '/data/chlamy_objchlamy.csv', sep = ''))
      
      #Simplify
      tmp = data.frame(species = rep(n[j], nrow(tmp)),
                       cell = rep(name, nrow(tmp)),
                       image_number = tmp$ImageNumber,
                       object_number = tmp$ObjectNumber,
                       x = tmp$Location_Center_X,
                       y = tmp$Location_Center_Y,
                       area = tmp$AreaShape_Area,
                       eccentricity = tmp$AreaShape_Eccentricity,
                       radius = tmp$AreaShape_MeanRadius,
                       minor_axis = tmp$AreaShape_MinorAxisLength,
                       major_axis = tmp$AreaShape_MajorAxisLength,
                       perimeter = tmp$AreaShape_Perimeter)
      
      #Split on object
      tmp = split(tmp, tmp$object_number)
      
      #Add to list
      for(h in 1:length(tmp)){
        
        if(nrow(tmp[[h]])>experiment_length_cutoff){
          
          #Add velocity
          velocity =  c(sqrt(diff(tmp[[h]]$x, lag = 20)^2 + diff(tmp[[h]]$y, lag = 20)^2), rep(NA, 20))
          velocity = ksmooth(1:nrow(tmp[[h]]), velocity, bandwidth = 10)$y
          
          angle = atan2(diff(tmp[[h]]$y, lag = 20), diff(tmp[[h]]$x, lag = 20))*(180/pi)
          angle = ksmooth(1:nrow(tmp[[h]]), angle, bandwidth = 10)$y
          
          tmp[[h]]$velocity = velocity
          tmp[[h]]$angular_velocity = abs(angle)
          
          tmp[[h]]$cell = rep(paste(name, h, sep = '-'), nrow(tmp[[h]]))
          
          objs[[paste(name, h, sep = '-')]] = tmp[[h]]
        }
      }
    }
  }
  
  #Return
  return(objs)
}


#Function to plot 2D comparison of angular and forward velocity
plot_velocity_prob_density_function = function(velocity,
                                               angular_velocity,
                                               pdf_lims = c(c(0, 140), c(0, 200)),
                                               pdf_n = 300,
                                               title_label = NULL,
                                               xlab = 'Angular velocity',
                                               ylab = 'Velocity',
                                               ...){
  
  #Calculate
  pdf = kde2d(velocity,
              angular_velocity,
              lims = pdf_lims,
              n = pdf_n,
              ...)
  
  #Plot
  image(pdf, 
        xlab = xlab,
        ylab = ylab,
        cex.lab = 1.5,
        cex.axis = 1.5)
  if(is.null(title_label) == FALSE){
    title(main = title_label, font.main = 1, cex.main = 1.5)
  }
  
  #Return pdf
  return(pdf)
}

#Function to plot difference between 2 probability density functions
plot_diff_prob_density_function = function(pdf_1,
                                           pdf_2,
                                           col1 = 'midnightblue',
                                           col2 = 'darkred'){
  
  #Subtract pdf1 from pdf2
  d = pdf_1$z/max(pdf_1$z) - pdf_2$z/max(pdf_2$z)
  
  #Round
  d = round(d, 2)
  
  #Get colors
  col1 = colorRampPalette(c(col1, 'white'))(length(seq(min(d), 0, 0.01)))
  col2 = colorRampPalette(c('white', col2))(length(seq(0.01, max(d), 0.01)))
  cols = c(col1, col2)
  
  #Plot
  image(d,
        xlab = 'Angular velocity',
        ylab = 'Velocity',
        col = cols,
        cex.axis = 1.5,
        cex.lab = 1.5,
        xaxt = 'n',
        yaxt = 'n')
  axis(1, seq(0, 1, 1/7), seq(0, 140, 20), cex.axis = 1.5)
  axis(2, seq(0, 1, 1/4), seq(0, 200, 50), cex.axis = 1.5)
  title(main = 'Difference', font.main = 1, cex.main = 1.5)
  
  #Return difference
  return(d)
}