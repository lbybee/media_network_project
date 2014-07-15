from numpy import *

def processWords(word):
    """returns vector of letters in vocab"""

    return


def alphaPost(alpha_n1, gamma_i, delta2, a2 theta_dit, I, d_it):
    """generates the full conditional for alpha_it
    
    delta2: scalar
    a2: scalar
    I: NxN identity matrix
    d_it: scalar, the number of documents for a given node in a given period
    alpha_it: NxK matrix of proportions for each node.  Each row is a node and each column is a proportion
    gamma_i: Nx1 vector, each element is a weight for that node
    theta_dit: DxK matrix of draws for each document.  Each row is the document and each column is the topic

    """

    # NOTE: multiplying lambda_ait * ... may not have the desired effect, this likely will need to be
    # fixed in testing

    lambda_ait = linalg.inv(1 / delta2 * I + d_it / a2 * I)
    mu_ait = lambda_ait * (1 / delta2 * I * dot(alpha_it * gamma_i) + d_it / a2 * I *  sum(theta_dit))
    return random.multivariate_normal(mu_ait, lambda_ait)


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

