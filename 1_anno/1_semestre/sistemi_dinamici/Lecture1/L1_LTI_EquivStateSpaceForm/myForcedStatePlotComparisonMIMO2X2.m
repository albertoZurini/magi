function myForcedStatePlotComparisonMIMO2X2(X1SET, X2SET, X3SET, TimeSET)
% myForcedOutputPlotComparison:
% plot the components of the step state responses X1SET, X2SET and X3SET
% using a subplot for each output component
%

Tfinal = TimeSET(end);
color1 = [0 0.4470 0.7410];
color2 = [0.8500 0.3250 0.0980];
color3 = [0.9290 0.6940 0.1250];

figure('Name','Compare forced state movements', ...
       'Units','normalized', 'Position', [0.1, 0.1, 0.8, 0.8]);

subplot(3,2,1);
plot(TimeSET, X1SET(:,1,1), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('State $x_1(k)$', 'Interpreter','latex');
title('State variable $x_1$ - input $u_1$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,1,1), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,1,1), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---

subplot(3,2,2);
plot(TimeSET, X1SET(:,1,2), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('State $x_1(k)$', 'Interpreter','latex');
title('State variable $x_1$ - input $u_2$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,1,2), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,1,2), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---
subplot(3,2,3);
plot(TimeSET, X1SET(:,2,1), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex');
ylabel('State $x_2(k)$', 'Interpreter','latex');
title('State variable $x_2$ - input $u_1$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,2,1), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,2,1), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---

subplot(3,2,4);
plot(TimeSET, X1SET(:,2,2), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('State $x_2(k)$', 'Interpreter','latex');
title('State variable $x_2$ - input $u_2$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,2,2), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,2,2), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---

subplot(3,2,5);
plot(TimeSET, X1SET(:,3,1), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('State $x_3(k)$', 'Interpreter','latex');
title('State variable $x_3$ - input $u_1$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,3,1), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,3,1), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---
subplot(3,2,6);
plot(TimeSET, X1SET(:,3,2), "LineStyle", "none", "Marker", "o", ...
    "MarkerSize",16, "MarkerFaceColor",color1, ...
    "DisplayName",'original system');
xlabel('Time instants [s]', 'Interpreter','latex'); 
ylabel('State $x_3(k)$', 'Interpreter','latex');
title('State variable $x_3$ - input $u_2$', 'Interpreter','latex');
set(gca, 'FontSize', 16);
grid on; hold on
plot(TimeSET, X2SET(:,3,2), "LineStyle", "none", "Marker", "square", ...
    "MarkerSize",12, "MarkerFaceColor",color2, ...
    "DisplayName",'manually transf. system');
plot(TimeSET, X3SET(:,3,2), "LineStyle", "none", "Marker", "diamond", ...
    "MarkerSize",10, "MarkerFaceColor",color3, ...
    "DisplayName",'MATLAB transf. system');
legend('Location','bestoutside');
% --- set the X axis limits
curr_ax = axis;
curr_ax(4)= curr_ax(4)+1e-1; curr_ax(2)= Tfinal; 
axis(curr_ax);
% ---

end