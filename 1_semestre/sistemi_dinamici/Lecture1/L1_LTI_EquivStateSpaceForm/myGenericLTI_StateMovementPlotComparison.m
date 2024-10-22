function myGenericLTI_StateMovementPlotComparison(XD, T_XD, TimeSET)
% myGenericLTI_StateMovementPlotComparison:
% plot the components of the state responses XD and T_XD
% using a subplot for each state component
%

Tfinal = TimeSET(end);
color1 = [0 0.4470 0.7410];
color2 = [0.8500 0.3250 0.0980];
color3 = [0.9290 0.6940 0.1250];

figure('Name','Compare free state movements',...
        'Units','normalized', 'Position', [0.1, 0.1, 0.6, 0.99]);

[m, n] = size(XD);
% m <-- # of time instants
% n <-- # of state variables

for i =1:n
    subplot(n,1,i);
    plot(TimeSET, XD(:,i), 'square-',  "MarkerSize", 14 , "MarkerFaceColor", color1, "MarkerEdgeColor", color1); 
    hold on;
    plot(TimeSET, T_XD(:,i), 'diamond-.', "MarkerSize", 8 , "MarkerFaceColor", color2, "MarkerEdgeColor", color2 ); 
    grid on; zoom on
    xlabel('Time instants'); ylabel(['State variable $x_',num2str(i),'(k)$'], 'Interpreter','latex');
    if (i==1), title('Comparison of State Movements'); end % if
    legend('original system repr.', 'new system repr.', 'Location','bestoutside');
    set(gca, 'FontSize', 16);
end % for i

end