function dxdt = cart_pend_for(t, x, g, mp, mc, l, mu_p, U)

  dxdt = zeros(4,1);

  dxdt(1) = x(2);
  dxdt(2) = (U+mp*l*((x(4)^2)*sin(x(3))-((g*sin(x(3))+ cos(x(3))*((-U-mp*l*(x(4)^2)*sin(x(3)))/(mc+mp))-((mu_p*x(4))/(mp*l)))/(l*((4/3)-((mp*cos(x(3))^2)/(mc+mp)))))*cos(x(3))))/(mc+mp);
  dxdt(3) = x(4);
  dxdt(4) = (g*sin(x(3))+ cos(x(3))*((-U-mp*l*(x(4)^2)*sin(x(3)))/(mc+mp))-((mu_p*x(4))/(mp*l)))/(l*((4/3)-((mp*cos(x(3))^2)/(mc+mp))));

end