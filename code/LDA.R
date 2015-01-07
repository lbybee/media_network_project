load("DTM.RData")

library(tm)
library(topicmodels)

# initalize the number of topics
K <- 50
Kstp <- 5
Kstart <- 5 

# This takes in a cleaned DTM with term frequency
# The DTM should be the only thing in DTM.RData

for(k in seq(Kstart, K, Kstp)){

    ts <- proc.time()
    topic_model <- LDA(dtm, k)
    tf <- proc.time() - ts
    print(tf)
    save.image(paste("LDA", k, "RData", sep="."))
}

