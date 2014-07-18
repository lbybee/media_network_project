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

res = gamma_mcmc.alphaPost(alpha_n1, gamma_i, delta2, a2, theta_it, I, d_it)

# betaPost test
