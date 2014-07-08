import numpy as np


def postBetaLog(phi, beta_t, beta_tn1):
    """generates the log proposed value for a proposal beta_t"""

    prior = np.dot((beta_t - beta_tn1).T, (beta_t - beta_tn1))
    like = 0.0
    for phi_k in phi:
        like += np.dot((phi_k - beta_t).T, (phi_k - beta_t))
    return like + prior


def postAlphaLog(theta, alpha_it, gamma_i, alpha_tn1):
    """generates the log proposed value for a proposal alpha_it"""

    # NOTE: The set up on all these is important.  alpha_tn1 is a KxN matrix, where K is the number of topics and N is the number of agents.  gamma_i is a Nx1 array. alpha_tn1 is a Kx1 array.

    prior = np.dot((alpha_it - np.squeeze(np.dot(alpha_tn1, gamma_i))).T, (alpha_it - np.squeeze(np.dot(alpha_tn1, gamma_i))))
    like = 0.0
    for theta_d in theta:
        like += np.dot((theta_d - alpha_it).T, (theta_d - alpha_it))
    return like + prior


def postGammaLog(alpha_i, gamma_i, alpha_n1, mu):
    """generates the log proposed value for a proposal gamma_i"""

    # NOTE: alpha_n1 is a list of the PRIOR period values for alpha_t, alpha_i is a list of the current values for alpha_it

    prior = np.dot((gamma_i - mu).T, (gamma_i - mu))
    like = 0.0
    for a_it, a_tn1 in zip(alpha_i, alpha_n1):
        like += np.dot((a_it - np.squeeze(np.dot(a_tn1, gamma_i))).T, (a_it - np.squeeze(np.dot(a_tn1, gamma_i))))
    return like + prior
