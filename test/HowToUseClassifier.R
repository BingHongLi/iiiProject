library(party)
ind <- sample(2,nrow(test),replace=T,prob=c(0.5,0.5))

myFomula <- CLARA~Accounting+Action+Adventure+Casual+Indie+Racing+RPG+Simulation+Sports+Strategy+Utilities  
#myFomula <- CLARA~.

trainData <-test[ind==1,]
testData <- test[ind==2,]
#test_ctree <- ctree(myFomula,data=trainData)
test_ctree <- ctree(myFomula,data=CLUSTER12)

plot(test_ctree)
print(test_ctree)

library(rpart)
myFomula <- CLARA~Accounting+Adventure+Casual+Education+Indie+Racing+RPG
test_rpart <- rpart(myFomula,data=CLUSTER12,control=rpart.control(minsplit=10))
plot(test_rpart)
text(test_rpart,use.n=T)


library(tree)
treeModel <- tree(CLARA~Accounting+Adventure+Casual+Education+Indie+Racing+RPG,data=CLUSTER12)
plot(treeModel)
text(treeModel)

########################################################################################
library(rpart)
library(rpart.plot)
C1 <- ALLCLUSTER[which(ALLCLUSTER[,3]==1),]
C2 <- ALLCLUSTER[which(ALLCLUSTER[,3]==12),]
C3 <- ALLCLUSTER[which(ALLCLUSTER[,3]==13),]
C4 <- ALLCLUSTER[which(ALLCLUSTER[,3]==14),]
C5 <- ALLCLUSTER[which(ALLCLUSTER[,3]==16),]
PREPAREANALYSIS <- rbind(C1,C2,C3,C4,C5)
myFomula <- CLARA~Accounting+Adventure+Casual+Education+Indie+Racing+RPG
test_rpart <- rpart(myFomula,method="class",data=PREPAREANALYSIS,control=rpart.control(minsplit=10))
plot(test_rpart)
text(test_rpart,use.n=T)
rpart.plot(test_rpart)