from numpy import *
from datetime import datetime
from scipy import stats

def alphaPost(gamma_ii, delta2, sigma2, xi, theta_is, I, T):
    """generates the posterior estimate for the ith alpha
    
    * delta2: scalar
    * I: KxK identity matrix
    * gamma_ii: scalar the weight of the ith element on itself
    * theta_is: theta_i.sum(axis=0)
    * theta_i: TxK matrix of draws for each document.  Each row is the
    document and each column is the topic

    NOTES:

    * theta_i.sum(axis=0) sums all the columns so you get a Kx1 vector
    that is the sum of thetas over the documents

    * lambda_ai is a KxK matrix of the covariance
    * mu_ai is a Kx1 vector for the mean
    
    """

    lambda_ai = I * (1 / (1 / sigma2 + gamma_ii ** 2 / delta2))
    mu_ai = (xi / sigma2 * I + (T * gamma_ii * theta_is) / delta2)
    mu_ai = dot(transpose(lambda_ai), mu_ai)
    return random.multivariate_normal(mu_ai, lambda_ai)


def gammaPost(alpha, chi2, delta2, eta, theta_is, I, T):
    """generates the posterior estimate for the ith gamma"""

    lambda_gi = linalg.inv(1 / chi2 * I + dot(alpha, transpose(alpha)) / delta2)
    mu_gi = (eta / chi2 * I + (T * dot(alpha, theta_is)) / delta2)
    mu_gi = dot(transpose(lambda_gi, mu_gi))
    return random.multivariate_normal(mu_gi, lambda_gi)


def phiPost(beta, w_k):
    """generates the posterior estimate for phi_k

    * vector of word indices
    * beta: Vx1 vector

    """

    for w in w_k:
        beta[w] += 1
    return random.dirichlet(beta)


def zPost(theta_it, w, phi):
    """
    
    * theta_it: Kx1 vector of proportions for topics
    * w: Vx1 vector where the 1 value corresponds to the word
    * phi: KxV matrix.  We iterate through the topics here and then take the correct
    vocab for w.
    
    """
    
    l_theta_it = len(theta_it)
    theta_phi = zeros(l_theta_it)
    i = 0
    for theta_itk, phi_k in zip(theta_it, phi):
        theta_phi[0] = (theta_itk / sum(theta_it)) * (phi_k[w] / sum(phi_k))
        i += 1
    return random.multinomial(1, theta_phi)


def logitNormalSampler(z, theta_it, alpha, gamma_i, delta2):
    """generates a augmented variable sample for theta/phi, this is a general
    function since they both have the same form.
    
    * z: WxK matrix.  This is a vector of the topics chosen for each of the W
    words.
    * theta_it: Kx1 vector.  This is an array of each of the proportions
    for the given document.  The result of this function is just an updated
    version of this.
    * alpha_it: Kx1 vector.  This is the underlying proportions.
    * delta2: scalar.
    
    
    """

    l_z = len(z)
    l_theta_it = len(theta_it)
    theta_itp = zeros(l_theta_it)
    for i, theta_kit in enumerate(theta_it):
        un_l = array([nan for u in range(l_z)]) 
        un_u = array([nan for u in range(l_z)])
        for j, z_w in enumerate(z):
            if z_w[i] == 1:
                un_l[j] = random.uniform(0, exp(theta_kit) / exp(sum(theta_it)))
            else:
                un_u[j] = random.uniform(exp(theta_kit) / exp(sum(theta_it)), 1)
        mx_mn = max(un_l)
        mn_mx = min(un_u)
        theta_itp[i] = stats.truncnorm.rvs(mx_mn, mn_mx, sum(alpha[:,i] * gamma_i[i]), delta2)
    return theta_itp


def genVocab(graph, z, K):
    """generates the vocab for phi"""
    
    vocab = [[] for i in range(K)]
    for z_g, node in zip(z, graph):
        for z_n, docs in zip(z_g, node):
            for z_d, wrds in zip(z_n, docs):
                for z_w, w in zip(z_d, wrds):
                    vocab[where(z_w==1)[0][0]].append(w)
    return vocab


def fullRun(N, K, V, S, graph, xi, sigma2, delta2, eta, chi2):
    """does the full run"""

    # initalize values
    gamma = array([[1. / N for i in range(N)] for i in range(N)])
    alpha = array([[1. for k in range(K)] for i in range(N)])
    phi = array([[1. for v in range(V)] for k in range(K)])
    theta = array([[1. for t in range(len(node))] for node in graph])
    z = array([[[1 for w in range(len(date))] for date in node] for node in graph])
    print "values initalized"

    # initalize storage
    gamma_s = array([[[nan for i in range(N)] for i in range(N)] for s in range(S)])
    alpha_s = array([[[nan for k in range(K)] for i in range(N)] for s in range(S)])
    phi_s = array([[[nan for v in range(V)] for k in range(K)] for s in range(S)])
    theta_s = array([[[nan for t in range(len(node))] for node in graph] for s in range(S)])
    z_s = array([[[[nan for w in range(len(date))] for date in node] for node in graph] for s in range(S)])
    print "storage initalized"

    # initialize start time
    t_1 = datetime.now()

    for s in range(S):

        for i in range(N):

            I = identity(N)

            T = len(graph[i])

            theta_is = theta[i].sum(axis=0)

            gamma_s[s][i] = gamma[i]
            gamma[i] = gammaPost(alpha, chi2, delta2, eta, theta_is, I, T)

            I = identity(K)

            alpha_s[s][i] = alpha[i]
            alpha[i] = alphaPost(gamma[i][i], delta2, sigma2, xi, theta_is, I, T)

            for t in range(len(graph[i])):

                I = identity(K)
                w_it = len(graph[i][t])

                theta_s[s][i][t] = theta[i][t]
                theta[i][t] = logitNormalSampler(z[i][t], theta[i][t], alpha, gamma[i], delta2)

                for w in range(w_it):

                    z_s[s][i][t][w] = z[i][t][w]
                    z[i][t][w] = zPost(theta[i][t], graph[i][t][w], phi)
        
        I = identity(V)
        vocab = genVocab(z, graph)

        for i in range(K):

            phi_s[s][k] = phi[k]
            phi[k] = phiPost(beta, vocab[k])

        print datetime.now() - t_1, (s * 100.) / S

    return gamma_s, alpha_s, phi_s, theta_s, z_s
