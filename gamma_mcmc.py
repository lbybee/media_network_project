from numpy import *
from datetime import datetime

def processWords(word):
    """returns vector of letters in vocab"""

    return


def alphaPost(alpha_n1, gamma_i, delta2, a2, theta_it, I, d_it):
    """generates the full conditional for alpha_it
    
    * delta2: scalar
    * a2: scalar
    * I: KxK identity matrix
    * d_it: scalar, the number of documents for a given node in a given
    period
    * alpha_n1: NxK matrix of proportions for each node.  Each row is a
    node and each column is a proportion
    * gamma_i: Nx1 vector, each element is a weight for that node
    * theta_it: DxK matrix of draws for each document.  Each row is the
    document and each column is the topic
    * mu_ait: Kx1 vector

    NOTES:

    * theta_it.sum(axis=0) sums all the columns so you get a Kx1 vector
    that is the sum of thetas over the documents
    * dot(alpha_n1, gamma_i) is a Kx1 vector for the "mean".
    * 1 / delta2 * I is a KxK diagonal matrix with 1 / delta2 in the diagonal
    * d_it / a2 * I is a KxK diagonal matrix with d_it / a2 in the diagonal
    * dot(transpose(1 / delta2 * I), dot(transpose(alpha_n1), gamma_i)) is
    a Kx1 vector for the prior
    * dot(transpose(d_it / a2 * I), theta_it.sum(axis=0)) is a Kx1 vector
    for the data

    * lambda_ait is a KxK matrix of the covariance
    * mu_ait is a Kx1 vector for the mean

    """

    lambda_ait = linalg.inv(1 / delta2 * I + d_it / a2 * I)
    mu_ait = dot(transpose(lambda_ait), (dot(transpose(1 / delta2 * I),
                                             dot(transpose(alpha_n1), gamma_i))
                                         + dot(transpose(d_it / a2 * I),
                                               theta_it.sum(axis=0))))
    return random.multivariate_normal(mu_ait, lambda_ait)


def betaPost(beta_n1, sigma2, b2, phi_t, I, k):
    """generates the full conditional for beta_t

    * sigma2: scalar
    * b2: scalar
    * I: VxV identity matrix
    * k: scalar, the number of topics
    * beta_n1: Vx1 vector
    * phi_t: KxV matrix of proportions for each topic for each word.
    * mu_bit: Vx1 vector
    
    NOTES:

    * phi_t.sum(axis=0) sums all the columns so you get a Vx1 vector.
    The columns in this case are the topics.  There is a phi_tk for
    each topic.
    * See alphaPost notes.  It is basically the same.

    """

    lambda_bit = linalg.inv(1 / sigma2 * I + k / b2 * I)
    mu_bit = dot(transpose(lambda_bit), (dot(transpose(1 / sigma2 * I),
                                             beta_n1)
                                         + dot(transpose(k / b2 * I),
                                               phi_t.sum(axis=0))))
    return random.multivariate_normal(mu_bit, lambda_bit)


def gammaPost(alpha_i, alpha_n, xi2, eta, delta2, I):
    """generates the full conditional for gamma_i

    * xi2: scalar
    * delta2: scalar
    * I: NxN identity matrix
    * alpha_n: Tx(NXK) matrix of alpha_it-1 matricies.  alpha_it-1 is an
    NxK matrix of proportions for each node. Each row is a node and each
    column is a proportion
    * alpha_i: Tx(Kx1) matrix of alpha_it values.  alpha_it is a vector
    of the topic proportions for the ith node.
    * gamma_i: Nx1 vector, each element is a weight for that node
    * dot(alpha_n.sum(axis=0), transpose(alpha_n.sum(axis=0))): NxN matrix
    The transposes are different here from above because in order to get
    gamma we have to treat the rows as columns and columns as rows
    * dot(alpha_n.sum(axis=0), alpha_i.sum(axis=0)): Nx1 vector
    * eta: Nx1 vector, the prior for gamma_i
    * mu_gi: Nx1 vector

    NOTES:

    * The only thing wierd here is the transposes.  Just think that alpha_n
    and alpha_i were already transposed before being fed in.

    """

    lambda_gi = linalg.inv(1 / xi2 * I + dot(alpha_n.sum(axis=0),
                                             transpose(alpha_n.sum(axis=0)))
                           / delta2)
    mu_gi = dot(transpose(lambda_gi), (eta / xi2 + dot(alpha_n.sum(axis=0),
                                            alpha_i.sum(axis=0)) / delta2))
    return random.multivariate_normal(mu_gi, lambda_gi)


def zPost(theta_itd, w, phi_t):
    """
    
    * theta_itd: Kx1 vector of proportions for topics
    * w: Vx1 vector where the 1 value corresponds to the word
    * phi_t: KxV matrix.  We iterate through the topics here and then take the correct
    vocab for w.
    
    """
    
    theta_phi = array([])
    w_ind = where(w==1)[0][0]
    for theta_itdk, phi_tk in zip(theta_itd, phi_t):
        theta_phi.append((theta_itdk / sum(theta_itd)) * (phi_tk[w_ind] / sum(phi_tk)))
    return random.multinomial(1, theta_phi)


def logitNormalSampler(z, theta_dit, alpha_it, a2):
    """generates a augmented variable sample for theta/phi, this is a general
    function since they both have the same form.
    
    * z: WxK matrix.  This is a vector of the topics chosen for each of the W
    words.
    * theta_dit: Kx1 vector.  This is an array of each of the proportions
    for the given document.  The result of this function is just an updated
    version of this.
    * alpha_it: Kx1 vector.  This is the underlying proportions.
    * a2: scalar.
    
    NOTES:
    
    * This all works the same for the phis.  Where the thetas use documents,
    phis use topics, where thetas use topics phis use vocabulary.
    
    In the phi case:
    
    * w: WxV matrix.  This is just a matrix of the words, each word is a location
    in a vocab vector.
    * phi_kt.  Vx1 vector.  This is a vector of the proportion for each word
    for the kth topic.
    * beta_t: Vx1 vector.  This is the underlying proportions.
    * b2 scalar.

    """

    theta_ditp = array([])
    for i, theta_kdit in enumerate(theta_dit):
        un_l = array([])
        un_u = array([])
        for z_w in z:
            if z_w[i] == 1:
                un_l.append(random.uniform(0, exp(theta_kdit) / exp(sum(theta_dit))))
            else:
                un_u.append(random.uniform(exp(theta_kdit) / exp(sum(theta_dit)), 1))
        mx_mn = max(un_l)
        mn_mx = min(un_u)
        theta_ditp.append(stats.truncnorm.rvs(mx_mn, mn_mx, alpha_it[i], a2))
    return theta_ditp


def genPrevAlpha(alpha, T, N):
    """gets the previous alpha values"""

    # this essentially transposes the N and T values without changing the inner values
    alpha_n = array([[alpha[i, t] for i in range(N)] for t in range(T-1)])
    return alpha_n


def fullRun(N, K, T, V, iterations, graph, vocab, xi2, delta2): 

    # initalize values
    gamma = array([[1. / N for i in range(N)] for i in range(N)])
    alpha = array([[[1. for k in range(K)] for t in range(T)] for i in range(N)])
    beta = array([[1. for v in range(V)] for t in range(T)])
    phi = array([[[1. for v in range(V)] for k in range(K)] for t in range(T)])
    theta = array([[[[1. for d in range(len(docs))] for docs in period] for period in node] for node in graph])
    
    # initalize storage
    gamma_s = array([[[nan for i in range(N)] for i in range(N)] for s in range(S)])
    alpha_s = array([[[[nan for k in range(K)] for t in range(T)] for i in range(N)] for s in range(S)])
    beta_s = array([[[nan for v in range(V)] for t in range(T)] for s in range(S)])
    phi_s = array([[[[nan for v in range(V)] for k in range(K)] for t in range(T)] for s in range(S)])
    theta_s = array([[[[[nan for d in range(len(docs))] for docs in period] for period in node] for node in graph] for s in range(S)])
    z_s = array([[[[[[nan for w in range(len(wrds))] for wrds in range(len(docs))] for docs in period] for period in node] for node in graph] for s in range(S)])
    
    # initialize start time
    t_1 = datetime.now()

    # Now do the sampling
    for s in range(S):

        alpha_n = genPrevAlpha(alpha, T, N)
        
        for i in range(N):
          
            I = identity(N)

            gamma_s[s, i] = gamma[i]
            gamma[i] = gammaPost(alpha[i, 1:], alpha_n, xi2, mu, delta2, I)
            
            for t in range(1, T):

                I = identity(K)

                d_it = len(graph[i, t])

                alpha_s[s, i, t] = alpha[i, t]
                alpha[i, t] = alphaPost(alpha_n[t], gamma[i], delta2, a2, theta[i, t], I, d_it)

                for d in range(d_it):

                    w_it = len(graph[i, t, d])

                    theta_s[s, i, t, d] = theta[i, t, d]
                    theta[i, t, d] = logitNormalSampler(z[i, t, d], theta[i, t, d], theta[i, t], alpha[i, t], a2, I)

                    for w in range(w_it):

                        z_s[s, i, t, d, w] = z[i, t, d, w]
                        z[i, t, d, w] = zPost(theta[i, t, d], graph[i, t, d, w], phi[t])


        for t in range(1,T):

            I = identity(V)

            beta_s[s, t] = beta[t]
            beta[t] = betaPost(beta[t-1], sigma2, b2, phi[t], I, k)

            for k in range(K):

                phi_s[s, t, k] = phi[t, k]
                phi[t, k] = logitNormalSampler(vocab[t, k], phi[t, k], phi[t], beta[t], b2, I)

        print datetime.now() - t_1, (s * 100.) / S

    return gamma_s, alpha_s, beta_s, phi_s, theta_s
