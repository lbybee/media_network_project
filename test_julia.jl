use MCMC

modelxpr = quote
    v ~ Normal(0, 1)
    k ~ Normal(v, 1)
end

mymodel = model(modelxpr, k=ones(3))
