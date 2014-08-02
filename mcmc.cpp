using namespace Rcpp;   // inline does that for us already

int N = as<int>(n);

int addition (int a, int b)
{
    int r;
    r = a + b;
    return r;
}

NumericMatrix mat(2, 2);

int test;

mat(0,0) = 1;
mat(0,1) = 2;
mat(1,0) = 3;
mat(1,1) = 1;

test = addition(1, 2);

return test;             // Return to R
