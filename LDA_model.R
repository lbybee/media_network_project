library(tm)
library(topicmodels)
library(ggplot2)
library(MASS)

tab <- read.csv("8-21-2014_node_data.csv", header=FALSE)

# fix datetime
tab[,2] <- as.POSIXct(tab[,2])

# order by node and date
tab <- tab[order(tab[,1], tab[,2]),]

# save empty data
save.image("EmptyData.RData")

# make the corpus
vect <- VectorSource(tab[,3])
corpus <- Corpus(vect)

# clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, stripWhitespace)

# generate document term matrix
dtm <- DocumentTermMatrix(corpus)

# save the document term matrix data
save.image("DTM.RData")

model = LDA(dtm, 20)

# save the model image
save.image("20_Topic_LDA.RData")

# correlation code
K <- 20
xi2 <- 20
delta2 <- 20
eta <- 0

# ols code

nodes <- unique(tab[,1])
ln_nodes <- length(nodes)
stp <- length(tab[,1]) / ln_nodes

# convert topics into mat
top_mat <- matrix(NA, ln_nodes, stp)
topics <- topics(model)
for(i in 1:ln_nodes){
    for(j in 1:stp){
        top_mat[i, j] <- topics[(i - 1) * ln_nodes + j]
    }
}

# conditional prob
cond_prob_mat <- matrix(NA, ln_nodes, ln_nodes)
# most likely topic in each date node pair


# iterate through nodes
for(i in 1:ln_nodes){
    for(j in 1:ln_nodes){
        i_d <- top_mat[i, 2:stp]
        j_d <- top_mat[j, 1:(stp-1)]
        ln_data <- length(i_d)
        cond_prob_mat[i, j] <- sum(i_d == j_d) / ln_data
    }
}


# generate truth value
truth_ind <- matrix(NA, K, stp - 1)

for(i in 1:K){
    for(j in 2:stp){
        truth_ij <- 0
        prev_ind <- which(top_mat[,j-1] == i)
        curr_ind <- which(top_mat[,j] == i)
        for(k in curr_ind){
            belief <- 1
            for(q in prev_ind){
                belief <- belief * (1 - cond_prob_mat[k, q])
            }
            truth_ij <- truth_ij + belief
        }
        truth_ij <- truth_ij / ln_nodes
        truth_ind[i, j - 1] <- truth_ij
    }
} 
            
# generate depedent truth
truth_dep <- matrix(NA, K, stp - 1)
for(i in 1:K){
    for(j in 2:stp){
        truth_dep[i, j - 1] <- sum(top_mat[,j] == i) / ln_nodes
    }
}


# generate the risk for a node for each period
topic_risk <- list()
for(i in 1:K){
    t_mat <- matrix(NA, ln_nodes, stp - 1)
    for(j in 2:stp){
        prev_ind <- which(top_mat[,j - 1] == i)
        for(k in 1:ln_nodes){
            node_risk <- sum(cond_prob_mat[k, prev_ind])
            t_mat[k, j - 1] <- node_risk
        }
    }
    topic_risk[[i]] <- t_mat
}


# prduces expected value in each pair
expected_val_mat <- matrix(NA, ln_nodes, stp - 1)

for(i in 1:ln_nodes){
    for(j in 2:stp){
        mx <- 0
        mx_ind <- 1
        for(k in 1:K){
            if(topic_risk[[k]][i, j - 1] > mx){
                mx <- topic_risk[[k]][i, j - 1]
                mx_ind <- k
            }
        }
        expected_val_mat[i, j - 1] <- mx_ind
    }
}

            
# quality of firm
influence <- rep(NA, ln_nodes)
for(i in 1:ln_nodes){
    influence[i] <- sum(cond_prob_mat[,i])
}


# initalize storage
reg_l <- list()
p_l <- list()

# iterate through the nodes
for(i in 1:K){
    reg_mat <- matrix(NA, ln_nodes, ln_nodes)
    p_mat <- matrix(NA, ln_nodes, ln_nodes)
    for(j in 1:ln_nodes){
        D <- model@gamma[,i][((j-1)*stp + 2):(j*stp)]
        reg_data <- data.frame(D)
        for(k in 1:ln_nodes){
            reg_data[paste("I", k, sep="")] <- model@gamma[,i][((k-1)*stp + 1):(k*stp -1)]
        }
        mod <- glm(D ~ ., data=reg_data, family=binomial(logit))
        for(k in 1:ln_nodes){
            reg_mat[j, k] <- coef(summary(mod))[,1][k]
            p_mat[j, k] <- coef(summary(mod))[,4][k]
        }
    }
    reg_l[[i]] <- reg_mat
    p_l[[i]] <- p_mat
}


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
