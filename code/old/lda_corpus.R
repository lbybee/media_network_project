library(tm)
library(topicmodels)
library(SnowballC)
library(zoo)
library(topicmodels)

tab <- read.csv("8-3-2014-network_data_monthly.csv", header=FALSE)

tab <- tab[order(tab[,1]),]

# make the corpus
vect <- VectorSource(tab[,2])
corpus <- Corpus(vect)

# clean the corpus
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stemDocument)
corpus <- tm_map(corpus, stripWhitespace)

# add meta data (date)
meta(corpus, tag="date") <- tab[,1]

# make document term matrix
dtm = DocumentTermMatrix(corpus)
