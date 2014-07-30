# Compile and Load
testMat <- cxxfunction(signature(n="int"), paste( readLines( "mcmc.cpp" ), collapse = "\n"), plugin="Rcpp")
