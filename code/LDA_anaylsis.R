library(MASS)
library(ggplot2)
library(reshape)

genOLS <- function(model, K, lnnodes, stp, lag){
    # generates the OLS coefficients and p values for each K

    results <- list()
    results$coef <- list()
    results$pval <- list()

    for(i in 1:K){
        reg_mat <- matrix(NA, lnnodes, lnnodes)
        p_mat <- matrix(NA, lnnodes, lnnodes)
        for(j in 1:lnnodes){
            D <- model@gamma[((j-1)*stp + 1 + lag):(j*stp),i]
            reg_data <- data.frame(D)
            for(k in 1:lnnodes){
                reg_data[paste("I", k, sep="")] <- model@gamma[((k-1)*stp + 1):(k*stp - lag),i]
            }
            mod <- glm(D ~ ., data=reg_data, family=binomial(logit))
            reg_mat[j,] <- coef(summary(mod))[2:(lnnodes+1),1]
            p_mat[j,] <- coef(summary(mod))[2:(lnnodes+1),4]
        }
        results$coef[[i]] <- reg_mat
        results$pval[[i]] <- p_mat
    }
    return(results)
}


genMCMC <- function(model, K, ln_nodes, stp, xi2, delta2, eta){
    # generates the coefficients and p values for the MCMC estimate
    # for each K

    results <- list()

    # build data
    theta_n <- list()
    for (i in 1:(stp-1)){
        NK_mat <- matrix(NA, ln_nodes, K)
        for(j in 1:ln_nodes){
            NK_mat[j,] <- model@gamma[(i - 1) * ln_nodes + j,]
        }
        theta_n[[i]] <- NK_mat
    }

    # build theta
    theta <- list()
    for(i in 1:ln_nodes){
        theta_i <- matrix(NA, stp - 1, K)
        for(j in 2:stp){
            theta_i[j-1,] <- model@gamma[(j - 1) * ln_nodes + i,]
        }
        theta[[i]] <- theta_i
    }

    I_N <- diag(ln_nodes)

    # mcmc results
    gamma <- matrix(NA, ln_nodes, ln_nodes)
    pval1 <- matrix(NA, ln_nodes, ln_nodes)
    pval2 <- matrix(NA, ln_nodes, ln_nodes)

    lambda_gi = solve(1 / xi2 * I_N + Reduce('+', theta_n) %*% t(Reduce('+', theta_n)))

    for (i in 1:ln_nodes){
        mu_gi <- t(lambda_gi) %*% (eta / xi2 + (Reduce('+', theta_n) %*% colSums(theta[[i]])) / delta2)
        samp <- mvrnorm(5000, mu_gi, lambda_gi)
        mn <- apply(samp, 2, mean)
        std <- apply(samp, 2, sd)
        tv <- mn / std
        pv1 <- apply(samp, 2, function(x) sum(x > 0) / dim(samp)[1])
        pv2 <- apply(samp, 2, function(x) sum(x < 0) / dim(samp)[1])
        gamma[i,] <- mn
        pval1[i,] <- pv1
        pval2[i,] <- pv2
    }    

    results$gamma <- gamma
    results$pval1 <- pval1
    results$pval2 <- pval2
    return(results)
}

lda_res_list <- list()

# initalize the number of topics
K <- 50
Kstp <- 5
Kstart <- 5 
Kseq <- seq(Kstart, K, Kstp)
Kln <- length(Kseq)

ind <- 1
for(k in Kseq){
    load(paste("LDA", k, "RData", sep="."))
    lda_res_list[[ind]] <- topic_model
    ind <- ind + 1
}



# input values
K <- 20
xi2 <- 20
delta2 <- 20
eta <- 0
L <- 4 

# make nodes, the length of nodes and the number of periods
nodes <- unique(tab[,1])
ln_nodes <- length(nodes)
stp <- length(tab[,1]) / ln_nodes


# now generate the OLS and MCMC results
olsres <- list()

for(i in 1:Kln){
    olsres[[i]] <- list()
    for(j in 1:L){
        olsres[[i]][[j]] <- genOLS(lda_res_list[[i]], Kseq[i], ln_nodes, stp, j)
        print(paste(i, j))
    }
}


for(i in 1:Kln){
    for(j in 1:L){
        dir.create(paste("sig.plots", i, j, sep="."))
        setwd(paste("sig.plots", i, j, sep="."))
        for(k in 1:Kseq[i]){
            coefdat <- olsres[[i]][[j]]$coef[[k]]
            pvaldat <- olsres[[i]][[j]]$pval[[k]]
            heatpltmat <- matrix(NA, ln_nodes, ln_nodes)
            rownames(heatpltmat) <- nodes
            colnames(heatpltmat) <- nodes
            heatpltmat[pvaldat < 0.01] <- 1
            heatpltmat[pvaldat >= 0.01] <- 0
            qplot(x=X1, y=X2, data=melt(heatpltmat), fill=value, geom="tile", alpha=0.4) +
                theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
                xlab("Independent") + ylab("Dependent") + 
                scale_fill_gradient(low="white", high="black") +
                theme(legend.position="none") 
                #scale_fill_continuous(name="Coef") #, limits=c(-0.0, 1.0))
            ggsave(filename=paste("sig.heatmap", i, j, k, "jpg", sep="."))
        }
        setwd("..")
    }
}

