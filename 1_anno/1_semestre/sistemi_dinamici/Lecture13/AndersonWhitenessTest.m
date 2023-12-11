function H = AndersonWhitenessTest(prediction_residuals, ...
                                    alpha_value, ...
                                    verboseFLAG)
% simple implementation of the Anderson's whiteness test 
% on 1-step-ahead prediction residual
% System Dynamics - 267MI - Fall 2023 - Univ. of Trieste
% G. Fenu

if (alpha_value >0) && (alpha_value<1)
    alpha = alpha_value;
else
    error(['AndersonWhitenessTest: the chosen confidence level ', ...
           'must be strickly positive and below 1']);
end

% how many data?
N = numel(prediction_residuals);
M = floor(N/20);
if verboseFLAG
    fprintf(1, ...
        'AndersonWhitenessTest: confidence level %f\n',...
        alpha);
    fprintf(1, ...
        'AndersonWhitenessTest: max lag value M %d\n',...
        M);
end
% the maximum value for lag, when evaluating 
% the sampled autocorrelation function (see SD L13 p30)
normAutocorrCoeffs = xcorr(prediction_residuals, ...
                            M, ...
                            'coeff');
% the normalized sampled autocorrelation function

% scaling the function values
scaled_hat_rho_coeffs = normAutocorrCoeffs * sqrt(N); 
% see SD L13 p30

% using the confidence level alpha, find the value beta such that
%               Prob{abs(x) > beta} = alpha
% where x is  gaussian r.v. with mean 0 and variance 1
beta = sqrt(2)*erfinv(alpha);
bag_of_values = find(abs(scaled_hat_rho_coeffs)<=beta);
P = numel(bag_of_values);
criticalValue = P/M;

if verboseFLAG
    fprintf(1, ...
        'AndersonWhitenessTest: critical value %g\n',...
        criticalValue);
end
if (criticalValue > alpha)
    H = P;
    % refuse the hypothesis that scaled_hat_rho_coeffs is a r.v.
    % distributed as a G(0, 1)
    if verboseFLAG
        fprintf(1, ...
            ['AndersonWhitenessTest: refuse the hypothesis --> \n',...
            'the prediction error is NOT a stationary \n',...
            'white noise stochastic process\n\n']);
    end
else
    H = 0;
    % accept the the hypothesis that scaled_hat_rho_coeffs is a r.v.
    % distributed as a G(0, 1)
       if verboseFLAG
        fprintf(1, ...
            ['AndersonWhitenessTest: accept the hypothesis --> \n',...
            'the prediction error IS a stationary \n',...
            'white noise stochastic process\n\n']);
    end
end

end % function

