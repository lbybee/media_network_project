import gamma_mcmc
from numpy import *

# alphaPost test

alpha_n1 = random.randint(1, 20, size=(20, 10))
gamma_i = random.rand(20)
delta2 = 10.
a2 = 10.
theta_it = 4 * random.randn(5, 10) + 25
I = identity(10)
d_it = 5

alpha_r = gamma_mcmc.alphaPost(alpha_n1, gamma_i, delta2, a2, theta_it, I, d_it)

# betaPost test

beta_n1 = random.randint(1, 20, size=200)
sigma2 = 10.
b2 = 10.
phi_t = 4 * random.randn(10, 200) + 25
I = identity(200)
k = 10

beta_r = gamma_mcmc.betaPost(beta_n1, sigma2, b2, phi_t, I, k)
