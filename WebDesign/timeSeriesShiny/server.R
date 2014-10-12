
### Loading slow
getPrice <- read.csv('./data/SPrice.csv')
getContent <- read.csv('./data/SProfile.csv',stringsAsFactors=F)

# findDevelpoer  x is SProfile, y is the developer we want to search. 
# and output is a data.frame, there have all game about the developer we want to search
# slow row search !!!
findDeveloperGameList <- function(x,y){
  allDeveloperGameList <- data.frame()
  for (i in 1:nrow(x)){
    if(x[i,5]==y){
      allDeveloperGameList <- rbind(allDeveloperGameList,x[i,])
    }
  }  
  allDeveloperGameList
}

# accroding to the developer's game list, we find all game price about the developer
# x is all gamePrice list
# do nrow(x) slow!!!
findDeveloperGamePrice <- function(x,y){
  allDeveloperGamePrice <- data.frame()
  for (i in 1:nrow(x)){
    if (x[i,1] %in% y[,1] ){
      allDeveloperGamePrice <- rbind(allDeveloperGamePrice,x[i,])
    }
  }
  allDeveloperGamePrice
}



# draw a timeseries curve,x is gameID, y is a gamePriceList 
drawCurve<- function(x,y){
  #seperatePrice <- y[which(y[,1]==x),]
  seperatePriceTimeSeries <- ts(y[which(y[,1]==x),][,3])
  plot.ts(seperatePriceTimeSeries,col="red",)
}

shinyServer(function(input,output){
  
  #findDeveloperGamePrice(getPrice,findDeveloperGameList(getContent,input$selectDeveloper))
  #findDeveloperGameList(getContent,input$selectDeveloper)  
  #nameList=developerGameList[,3]
  
  output$plotTS <- renderPlot(drawCurve(input$selectGames,findDeveloperGamePrice(getPrice,findDeveloperGameList(getContent,input$selectDeveloper))))  
  
  
})