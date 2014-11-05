#Return table: GameName, TimeSeries
getClusterData <- function(cluster, method="pamk_7", rD="./data/forCrashCLUSTERPRICE1639.csv", wd="E:/R/TimeSeries"){
  setwd(wd)
  srcData = read.csv(rD, header=T, sep=",")  
  #srcData[raw of record in the cluster, col with game's name and time series]
  rawData <- srcData[which(srcData[method] == cluster), c(1, 23:ncol(srcData))]  
  
  return(rawData)
}

#Return table: orgPrice, GameName, TimeSeries 
getOrgPData <- function(rawData, orgPD="./data/steamRegularPrice.csv", wd="E:/R/TimeSeries"){
  setwd(wd)
  orgPData = read.csv(orgPD, header=F, sep=",")  
  
  orgPrice <- rep(NA, nrow(rawData)) #Create a vector of orgPrice(original price) as the column in fullData.
  fullData <- cbind(orgPrice, rawData) 
  for(i in 1:nrow(orgPData)){ 
    rowInFD = which(fullData[,2] == as.character(orgPData[i,1])) #Catch the row number which has record in data of original price.
    fullData[rowInFD ,1] = orgPData[i ,2] #Put the original price value into fullData
  }  
  return(fullData)
}

#Return table: orgPrice, GameName, TimeSeries(cut interval)
#startCol = 2 #Time series start from the 3rd column.
#start = startCol + 1 
#end = startCol + 385
getInterval <- function(fullData, end, start=1, tsStart=2){
  cut <- na.omit(cbind(fullData["orgPrice"] ,fullData[,(tsStart+start):(tsStart+end)])) #Combine the orgPrice with time interval for analyzing, and remove the record with NA.  
  return(cut)
}

disClass <- function(x, class=5){
  if(!is.null(x) && !is.na(x)){  #If the input value is missing or null then return NA/NULL
    x = round(x, 2) * 100 #Transfer the value to percentage
    remainder = x %% class #Caculate the remainder
    if(floor(class/2)+1 > remainder && remainder > 0) #If the reminder < (class/2)+1  (approach 0)
      x = floor(x / class) * class #Classify to previous class.
    if(class > remainder && remainder >= floor(class/2)+1) #If the reminder > (class/2)+1  (approach next class)
      x = floor(x / class) * class + class #Classify to next class.
    x = as.character(x / 100) #Transfer the number to character.
  }  
  return(x)
}

#Return table: orgPrice, TimeSeries(cut interval)
getDiscountTag <- function(cut){
  #dis = cut[ncol(cut)] / cut["orgPrice"] #Calculate the discount of each time series from the final record.
  discount <- sapply(unlist((cut[ncol(cut)] / cut["orgPrice"]), use.name=F), disClass) #Turn the dis from numeric into nominal label.
  forAnalyze <- data.frame(cbind(discount, cut[,-1])) #Remove the original price from table of cut, and combine with discount as Classfied ID.
  return(forAnalyze)
}

getDiscount <- function(listName, clusterMethod="pamk_7", RDPath="./data/forCrashCLUSTERPRICE1639.csv", orgPDPath="./data/steamRegularPrice.csv", wd="E:/R/TimeSeries"){  
  gameName = listName$gameName
  clusterNumber = listName$clusterNumber
  day = listName$day
  
  rawData <- getClusterData(clusterNumber, method=clusterMethod, rD=RDPath, wd=wd)
  fullData <- getOrgPData(rawData, orgPD=orgPDPath, wd=wd)
  cut <- getInterval(fullData, end=day)
  forAnalyze <- getDiscountTag(cut)
  ct <- ctree(discount~., data=forAnalyze, controls=ctree_control(minsplit=30, minbucket=10, maxdepth=25))
  #plot(ct, ip_args=list(pval=FALSE), ep_args=list(digits=0))
  
  gameData <- cbind(discount=NA, rawData[which(rawData[1] == gameName),-1])
  pDiscount <- predict(ct, newdata=gameData)
  
  result <- c(day=day, discount=as.character(pDiscount))
  return(result)
}
