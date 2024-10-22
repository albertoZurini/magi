function myFreeOutputPlotComparisonMIMO2X2(Y1SET, Y2SET, Y3SET, TimeSET)
% myForcedOutputPlotComparison:
% plot the components of the free output responses Y1SET, Y2SET and Y3SET
% using a subplot for each output component
%

Tfinal = TimeSET(end);
color1 = [0 0.4470 0.7410];
color2 = [0.8500 0.3250 0.0980];
color3 = [0.9290 0.6940 0.1250];

figure('Name','Compare free response outputs', ...
       'Units','normalized', 'Position', [0.1, 0.1, 0.8, 0.8]);

subplot(2,1,1);
plot(TimeSET, Y1SET(:,1), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('Output $y_1(k)$', 'Interpreter','latex');
title('Output $y_1$ - free movement', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, Y2SET(:,1), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transformed system');
plot(TimeSET, Y3SET(:,1), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transformed system');
legend('Location','best');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---

subplot(2,1,2);
plot(TimeSET, Y1SET(:,2), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1);
grid on; hold on
plot(TimeSET, Y2SET(:,2), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2);
plot(TimeSET, Y3SET(:,2), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3);
xlabel('Time instants [s]', 'Interpreter','latex');
ylabel('Output $y_2(k)$', 'Interpreter','latex');
title('Output $y_2$ - free movement', 'Interpreter','latex');
set(gca, 'FontSize', 16);
legend('Original system', 'Manually transformed system', ...
       'MATLAB transformed system', 'Location','best');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---
end