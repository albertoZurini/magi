close all
clear all
clc
% Example of DP task

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%           Before executing the code run "install_mpt3.m"          %%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%Environment creation
rows=5;
columns=4;
sizex=1;
sizey=1;

obstacles=[2 2;2 3;4 1;5 1;4 3;4 4];
goals=[5 4];


movements=[0 0;1 0;-1 0;0 1;0 -1];
mov_costs=[0;1;1;1;1];

% Figure creation
figure
idx=0;
for i=1:rows
    for j=1:columns
        Poly{i,j}=Polyhedron('A',[eye(2);-eye(2)],'b',[sizex*i;sizey*j;-sizex*(i-1);-sizey*(j-1)]);
        if ismember([i j],obstacles,'rows')
            plot(Poly{i,j},'Color','k');
        else
            idx=idx+1;
            if ismember([i j],goals,'rows')
                plot(Poly{i,j},'Color','w');
                final(idx)=0;
            else
                plot(Poly{i,j},'Color','w');
                final(idx)=1e15;
            end
            good(idx,:)=[i j];
        end
        hold on
        
    end
end

initial=[1 1]; % initial state

% Insert robot and goal in the image
[img, ~, alphachannel]=imread('robot_1.png');
im_p=image([initial(1)*sizex-0.05 (initial(1)-1)*sizex+0.05 ],[ initial(2)*sizex-0.05 (initial(2)-1)*sizex+0.05],img,'AlphaData', alphachannel);
[img_goal, ~, alphachannel_goal]= imread('flag.png');
im_g = image([goals(1)*sizex-0.05 (goals(1)-1)*sizex+0.05 ],[ goals(2)*sizex-0.05 (goals(2)-1)*sizex+0.05],img_goal,'AlphaData', alphachannel_goal);

horizon=7;

% Cost table computation
cost(horizon+1,1:idx)=final;
for ii=horizon:-1:1
    for jj=1:idx
        for ll=1:size(movements,1)
            if not(ismember(good(jj,:),goals,'rows')) && ll==1                
                cost_temp(ll)=1e20;
            else
                temp(ll,:)=good(jj,:)+movements(ll,:);
                [log,id]=ismember(temp(ll,:),good,'rows');
                if log
                    cost_temp(ll)=cost(ii+1,id)+mov_costs(ll);
                else
                    cost_temp(ll)=1e15;
                end
            end
        end
        [cm,idmm]=min(cost_temp);
        action(ii,jj)=idmm;
        cost(ii,jj)=cm;
    end
end


% Execute the best policy following the results of DP
figure(1)
disp('Press a key !')  % Press a key here.You can see the message 'Paused: Press any key' in        % the lower left corner of MATLAB window.
pause;

pos(1,:)=initial;
for ii=1:horizon
    [~,jj]=ismember(pos(ii,:),good,'rows');
    pos(ii+1,:)=pos(ii,:)+movements(action(ii,jj),:);
    im_p.XData=im_p.XData+movements(action(ii,jj),1);
    im_p.YData=im_p.YData+movements(action(ii,jj),2 );
    figure(1)
    pause(1)
end