using namespace Rcpp;   // inline does that for us already

int N = as<int>(n);

NumericMatrix mat(2, 2);

mat(0,0) = 1;
mat(0,1) = 2;
mat(1,0) = 3;
mat(1,1) = 1;

return mat;             // Return to R
