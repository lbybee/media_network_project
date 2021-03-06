# load libraries
library(tm)

# load data
tab <- read.csv("20150106_R_ready_12.csv", header=FALSE)

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
#corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, stripWhitespace)

# generate document term matrix
dtm <- DocumentTermMatrix(corpus)

# save the document term matrix data
save.image("DTM.RData")

