#install.packages('party')
library(party)
rawData = read.csv("./data/AllSteam1639.csv", header=F, sep=",") #Read the Data of history price.
orgPData = read.csv("./data/steamRegularPrice.csv", header=F, sep=",") #Read the Data of original/regular price.

#Calculate Missing values of every column in data of history price.
NAinData = NULL
for(i in 1:ncol(rawData)){
  NAinData <- cbind(NAinData, length(which(is.na(rawData[,i]))))
}

#Combine the Data of history price and original price into fullData.
orgPrice <- rep(NA, nrow(rawData)) #Create a vector of orgPrice(original price) as the column in fullData.
fullData <- cbind(orgPrice, rawData) 
for(i in 1:nrow(orgPData)){ 
  rowInFD = which(fullData[,2] == as.character(orgPData[i,1])) #Catch the row number which has record in data of original price.
  fullData[rowInFD ,1] = orgPData[i ,2] #Put the original price value into fullData
}

#Define function of classifying discount order
#The argument "class" is the interval of disccount label, default = 5
#Used to transfer numeric label to nominal lebel
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

#Cut data into
#Choose the time start/end point 
startCol = 2 #Time series start from the 3rd column.
start = startCol + 1 
end = startCol + 385
cut <- na.omit(cbind(fullData["orgPrice"] ,fullData[,start:end])) #Combine the orgPrice with time interval for analyzing, and remove the record with NA.
#denominator should put orgPrice
dis = cut[ncol(cut)] / cut["orgPrice"] #Calculate the discount of each time series from the final record.
discount <- sapply(unlist(dis, use.name=F), disClass) #Turn the dis from numeric into nominal label.
forAnalyze <- data.frame(cbind(discount, cut[,-1])) #Remove the original price from table of cut, and combine with discount as Classfied ID.

#Create decision tree model
#first argument: ClassfiedID ~ Analyzed data
#data: data source
#controls: algorithm argument setting, should give a ctree_control object.
#minsplit: the minimum of record in each node(except final node).
#minbucket: the minimum of record in each final node.
#maxdepth: maximum depth of the tree. The default maxdepth = 0 means that no restrictions are applied to tree sizes.
ct <- ctree(discount~., data=forAnalyze, controls=ctree_control(minsplit=30, minbucket=10, maxdepth=25))
#Draw the decision tree
#ip_args: the plot setting of node.
#pval: reveal p value or not.
#ep_args: the plot setting of edge.
#ditits: the decimal point position of number.
plot(ct, ip_args=list(pval=FALSE), ep_args=list(digits=0))

#Test the model
pDiscount <- predict(ct)

#Accuracy
ac = (sum(discount == pDiscount)) / nrow(forAnalyze)
