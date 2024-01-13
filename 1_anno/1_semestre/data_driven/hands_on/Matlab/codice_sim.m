clear all
close all
clc


% constants definition
g = 9.8; % gravitational acceleration
mc = 1;   % cart mass [kg]
l = 0.5; % half-pole length [m]
mp = 0.1; % pole mass [kg]
mup = 0.000002; % pole friction coefficient

theta0 = 0;
x0 = 0; 
dot_x0 = 0;
dot_theta0 = 0;

t2=0;
conds=[theta0, dot_theta0, x0, dot_x0];
X_nl = conds';

load U
N=length(U);

u = U;
timestep = 0.02;

for i = 1:N
    t1 = t2;
    t2 = t2+timestep;
    time = [t1, t2];
    [t,state] = ode45(@(t,x)odefcncarpole(t, x, g, u(i), mp, l, mc, mup), time, conds);
    tp = find(t == t2);
    conds = state(tp,:);
    X_nl = [X_nl, conds'];
end

tfin = timestep*length(X_nl)-timestep;
figure()
subplot(2,2,1)
plot(0:timestep:tfin,X_nl(1,:))
subplot(2,2,2)
plot(0:timestep:tfin,X_nl(2,:))
subplot(2,2,3)
plot(0:timestep:tfin,X_nl(3,:))
subplot(2,2,4)
plot(0:timestep:tfin,X_nl(4,:))

function dx = odefcncarpole(t, x, g, F, mp, l, mc, mup)
    %cart and pole model
    dx = zeros(4,1);
    %theta=x(1)  pc=x(3)
    dx(1) = x(2); %w
    dx(2) = ((g*sin(x(1)))+(cos(x(1))*((-F-(mp*l*(x(2)^2)*sin(x(1))))/...
        (mc+mp)))-((mup*x(2))/(mp*l)))/(l*((4/3)-((mp*((cos(x(1)))^2))/(mc+mp))));    %dot w
    dx(3) = x(4); %vc
    dx(4) = (F+(mp*l*(((x(2)^2)*sin(x(1)))-((((g*sin(x(1)))+(cos(x(1))*((-F-(mp*l*(x(2)^2)*sin(x(1))))/(mc+mp)))-((mup*x(2))/(mp*l)))/...
        (l*((4/3)-((mp*((cos(x(1)))^2))/(mc+mp)))))*cos(x(1))))))/(mc+mp); %dot vc
end