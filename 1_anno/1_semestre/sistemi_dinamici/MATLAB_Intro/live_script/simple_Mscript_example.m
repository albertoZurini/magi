% --> simple_Mscript_example.m <--
%
% A simple M-file example, containing the script solving the 
% equation x = cos(x) by recursion.
%
%

% 1st approach
tic % <-- what does this command? try "help tic"
x = zeros(1,20); x(1) = pi/4;
n = 1; d = 1;
 while d > 0.001 & n < 20
    n = n+1; x(n) = cos(x(n-1));
    d = abs( x(n) - x(n-1) );
end
[n,x(n)]
toc % <-- what does this command? try "help toc"

% 2nd approach
tic
 xold = pi/4; n = 1; d = 1;
 while d > 0.001 & n < 20
    n = n+1; xnew = cos(xold);
    d = abs( xnew - xold );
    xold = xnew;
end
[n, xnew, d]
toc

% Q: what is the most efficient approach? Why?