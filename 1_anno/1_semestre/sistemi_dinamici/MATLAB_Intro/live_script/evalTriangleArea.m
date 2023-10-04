function A = evalTriangleArea(a,b,c)
% The function evalTriangleArea(a, b, c) 
% computes the area of a triangle whose
% sides have length a, b and c.
% Inputs:
%     a,b,c: Lengths of sides
% Output:
%     A: area of triangle
% Usage:
%     Area = evalArea(2,3,4);
% Written by XXX, MM/DD/YY.
s = (a+b+c)/2;
A = sqrt(s*(s-a)*(s-b)*(s-c));
end % function
%%%%%%%%% end of evalTriangleArea %%%%%%%%%%%