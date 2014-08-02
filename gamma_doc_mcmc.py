from numpy import *
from datetime import datetime
from scipy import stats

def alphaPost(gamma_ii, delta2, sigm2, xi, theta_i, I, T):
    """generates the posterior estimate for the ith alpha
    
    * delta2: scalar
    * I: KxK identity matrix
    * gamma_ii: scalar the weight of the ith element on itself
    * theta_i: TxK matrix of draws for each document.  Each row is the
    document and each column is the topic

    NOTES:

    * theta_i.sum(axis=0) sums all the columns so you get a Kx1 vector
    that is the sum of thetas over the documents

    * lambda_ai is a KxK matrix of the covariance
    * mu_ai is a Kx1 vector for the mean
    
    """

    lambda_ai = I * (1 / (1 / sigma2 + gamma_ii ** 2 / delta2))
    mu_ai = (xi / sigma2 * I + (T * gamma_ii * theta_i.sum(axis=0)) / delta2)
    mu_ai = dot(transpose(lambda_ai), mu_ai)
    return random.multivariate_normal(mu_ai, lambda_ai)
