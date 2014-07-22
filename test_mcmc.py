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

# gammaPost test

alpha_i = random.randint(1, 20, size=(15, 10))
alpha_n = random.randint(1, 20, size=(15, 20, 10))
xi2 = 10.
eta = random.rand(20)
delta2 = 10.
I = identity(20)

gamma_r = gamma_mcmc.gammaPost(alpha_i, alpha_n, xi2, eta, delta2, I)


# phi post test

vocab = zeros((30, 200))
for i, j in enumerate(random.randint(0, 200, size=(30))):
    vocab[i, j] = 1
phi_kt = 4 * random.randn(200) + 25
beta_t = random.randint(1, 20, size=(200))
b2 = 10.
I = identity(200)

phi_kt = gamma_mcmc.logitNormalSampler(vocab, phi_kt, beta_t, b2)

# theta post test

z = zeros((30, 10))
for i, j in enumerate(random.randint(0, 10, size=(30))):
    z[i, j] = 1
theta_dit = 4 * random.randn(10) + 25
alpha_it = random.randint(1, 20, size=(10))
a2 = 10.
I = identity(10)

theta_dit = gamma_mcmc.logitNormalSampler(z, theta_dit, alpha_it, a2)

# z post test

theta_dit = 4 * random.rand(10) + 25
phi_t = 4 * random.rand(10, 200) + 25
w = zeros(200)
w[random.randint(200)] = 1

z_r = gamma_mcmc.zPost(theta_dit, w, phi_t)

# full run test

N = 20
T = 15
K = 10
V = 200
S = 500

graph = array([[[[[0. for j in range(200)]
                  for w in range(random.randint(10, 300))]
                 for d in range(random.randint(1, 10))]
                for t in range(T)]
               for i in range(N)])

for i in range(N):
    for t in range(T):
        for d in range(len(graph[i][t])):
            for w in range(len(graph[i][t][d])):
                graph[i][t][d][w][random.randint(200)] = 1
    
res = gamma_mcmc.fullRun(N, T, K, V, S, graph, xi2, sigma2, delta2, b2, a2)
