% پیوست ۵ - تابع لجستیک در متلب
% Logistic function using the coefficients (B) estimated in SPSS (Table 3-11).
%
% Input:
%   X - matrix, one sample per row, columns:
%       1. Agec     (categorical, 5 categories: 1..5)
%       2. DMHx     (binary)
%       3. sms2cat  (binary)
%       4. pANDDMHX (binary)
%       5. pORsms2cat (binary)
%       6. sex      (binary)
%       7. sbp      (categorical, 4 categories: 1..4)
% Output:
%   p - column vector of probabilities (0..1) of CVD
function p = calculate_p_for_samples(X)
    agec_coeffs = [-2.257, -1.453, -1.267, -0.894, 0];  % Agec(5) is the reference -> 0
    sbp_coeffs  = [-1.261, -0.578, -0.294, 0];          % sbp(4)  is the reference -> 0
    beta_other  = [1.045, 0.227, -0.354, 0.230, 0.190]; % DMHx, sms2cat, pANDDMHX, pORsms2cat, sex
    intercept   = 0;  % NOTE: set this to the SPSS "Constant" if you want absolute risks

    num_samples = size(X, 1);
    z = zeros(num_samples, 1);
    p = zeros(num_samples, 1);

    for i = 1:num_samples
        Agec = X(i, 1);
        sbp  = X(i, 7);
        agec_beta = agec_coeffs(Agec);
        sbp_beta  = sbp_coeffs(sbp);
        other_vars = X(i, 2:6);
        z(i, 1) = intercept + agec_beta + sbp_beta + other_vars * beta_other';
        p(i) = 1 / (1 + exp(-z(i)));
    end
end
