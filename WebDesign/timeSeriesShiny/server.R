getPrice <- read.csv('./data/SPrice.csv')
getContent <- read.csv('./data/SProfile.csv',stringsAsFactors=F)
# findDevelpoer
findDeveloperProfile <- function(x,y){
  allEA <- data.frame()
  for (i in 1:nrow(x)){
    if(x[i,5]==y){
      allDeveloperProfile <- rbind(allEA,x[i,])
    }
  }  
  allDeveloperProfile
}

#找出遊戲價格
findDeveloperGamePrice <- function(x){
  allEAPrice <- data.frame()
  for (i in 1:nrow(x)){
    if (x[i,1] %in% getEA[,1] ){
      allDeveloperGamePrice <- rbind(allEAPrice,x[i,])
    }
  }
  allDeveloperGamePrice
}


#此處x放要畫的遊戲價格曲線
drawCurve<- function(x){
  seperatePrice <- getEAPrice[which(getEAPrice[,1]==x),]
  seperatePriceTimeSeries <- ts(seperatePrice[,3])
  plot.ts(seperatePriceTimeSeries,col="red",)
}

shinyServer(function(input,output){
  
    
  
  output$plotTS <- renderPlot(drawCurve(input$selectDeveloper))
  

  

  
  
  
})