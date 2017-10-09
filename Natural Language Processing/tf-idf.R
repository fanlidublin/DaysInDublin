# environment
library(tm)
library(proxy)
library(dplyr)

doc <- c( "The sky is blue.", "The sun is bright today.",
          "The sun in the sky is bright.", "We can see the shining sun, the bright sun." )

# create term frequency matrix using functions from tm library
doc_corpus <- Corpus( VectorSource(doc) )
control_list <- list(removePunctuation = TRUE, stopwords = TRUE, tolower = TRUE)
tdm <- TermDocumentMatrix(doc_corpus, control = control_list)

# print
( tf <- as.matrix(tdm) )

# idf
( idf <- log( ncol(tf) / ( 1 + rowSums(tf != 0) ) ) )

# diagonal matrix
( idf <- diag(idf) )

tf_idf <- crossprod(tf, idf)
colnames(tf_idf) <- rownames(tf)
tf_idf
