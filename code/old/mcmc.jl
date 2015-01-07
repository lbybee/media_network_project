using MCMC

"""test data"""
alpha = [[rand(K) for n in 1:N] for tt in 1:T]
gamma = [rand(N) for n in 1:N]

ex = quote
    [[alpha_it ~ MvNormal(transpose(gamma_i * alpha_tn), delta2) for (alpha_it, gamma_i) in zip(alpha_t, gamma)] for (alpha_t, alpha_tn) in zip(alpha[2:], alpha[1:T-1])]
