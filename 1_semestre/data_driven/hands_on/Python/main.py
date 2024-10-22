x1,x2,x3,x4 = None,None,None,None
d_x3 = x4
d_x4 = (g*sin(x3)+ cos(x3)*((-F-m_p*l*(x4**2)*sin(x3))/(m_c+m_p))-((mu_p*x4)/(m_p*l))) / (l*((4/3)-((m_p*(cos(x3)**2))/(m_c+m_p))))

d_x1 = x2
d_x2 = (F+m_p*l*((x4**2)*sin(x3)-d_x4*cos(x3)))/(m_c+m_p)