function colorSET = myPlotColorSet()
% myPlotColorSet():  the function creates an array of 7 RGB triplets, 
%                    defining the colors to use when drawning 
%                    2D line plots
% See 
% https://it.mathworks.com/help/matlab/creating_plots/specify-plot-colors.html

    RGB1triplet = [0 0.4470 0.7410]; 
    RGB2triplet = [0.8500 0.3250 0.0980]; 
    RGB3triplet = [0.9290 0.6940 0.1250]; 
    RGB4triplet = [0.4940 0.1840 0.5560]; 
    RGB5triplet = [0.4660 0.6740 0.1880]; 
    RGB6triplet = [0.3010 0.7450 0.9330]; 
    RGB7triplet = [0.6350 0.0780 0.1840]; 

    colorSET = [RGB1triplet; ...
                RGB2triplet; ...
                RGB3triplet; ...
                RGB4triplet; ...
                RGB5triplet; ...
                RGB6triplet; ...
                RGB7triplet];

end