from numpy import *

def processWords(word):
    """returns vector of letters in vocab"""

    return


def fullRun(N, K, T, V, iterations, graph, xi2, delta2): 

    # initalize values
    gamma = array([[1. / N for i in range(N)] for i in range(N)])
    alpha = array([[[1. for k in range(K)] for t in range(T)] for i in range(N)])
    beta = array([[1. for v in range(V)] for t in range(T)])
    phi = array([[[1. for v in range(V)] for k in range(K)] for t in range(T)])
    theta = array([[[[1. for d in range(len(docs))] for docs in period] for period in node] for node in graph])

    for j in iterations:
        for gamma_i, alpha_i, theta_i in zip(gamma, alpha, theta):
            # Gibbs sampling for gamma i
            lambda_gi = linalg.inv(linalg.inv(xi2) + transpose(alpha_n1) * linalg.inv(delta2) * alpha_n1)
            mu_gi = lambda_gi * (linalg.inv(xi2) * eta + transpose(alpha_n1) * linalg.inv(delta2) * alpha_i)
            gamma_i = random.multivariate_normal(mu_gi, lambda_gi)
            for alpha_it, 

