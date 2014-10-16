library(dtw)
dtwOmitNA <-function (x,y)
{
    a<-na.omit(x)
    b<-na.omit(y)
    return(dtw(a,b,distance.only=TRUE)$normalizedDistance)
}

## create a new entry in the registry with two aliases
pr_DB$set_entry(FUN = dtwOmitNA, names = c("dtwOmitNA"))

load('./R/allPrice.Rdata')
library(foreach)
rm(x)
rm(z)
rm(scsc)
x = c()
z = matrix(0, nrow=length(allPrice), ncol=length(allPrice), byrow=T)
#length(allPrice)
foreach(i = 1:length(allPrice), .combine='rbind') %dopar%  { 
    print(i)
    timestart = Sys.time()
    yi = min(c(scale(allPrice[[i]][which(!is.na(allPrice[[i]]))])))
    foreach(j = 1:length(allPrice), .combine='c') %do% {
        if(j <= i){
            z[i,j] = 0
        }
        else{
            yj = min(c(scale(allPrice[[j]][which(!is.na(allPrice[[j]]))])))
            if(yi == 'NaN'){
                if(yj == 'NaN'){
                    x = 0
                    z[i,j] = x
                }
                else{
                    x = dtwOmitNA(1, c(scale(allPrice[[j]][which(!is.na(allPrice[[j]]))])) - min(c(scale(allPrice[[j]][which(!is.na(allPrice[[j]]))]))) +1)
                    z[i,j] = x
                }
            }
            else if(yj == 'NaN'){
                x = dtwOmitNA(c(scale(allPrice[[i]][which(!is.na(allPrice[[i]]))])) - min(c(scale(allPrice[[i]][which(!is.na(allPrice[[i]]))]))) +1, 1)
                z[i,j] = x
            }
            else{
                x = dtwOmitNA(c(scale(allPrice[[i]][which(!is.na(allPrice[[i]]))])) - yi +1,c(scale(allPrice[[j]][which(!is.na(allPrice[[j]]))])) - yj +1)
                z[i,j] = x
            }
        }
    }
    timeend = Sys.time()
    print(timeend - timestart)
}
scsc= z
colnames(scsc) = names(allPrice)[1:length(allPrice)]
rownames(scsc) = names(allPrice)[1:length(allPrice)]
scscAll = (scsc) + t(scsc))*10

library(clue)
kmedoids(scscAll, k = 20)

library(cluster)
cluster = clara(scscAll, k = 20, metric = "manhattan", samples = 50, rngR = TRUE)
