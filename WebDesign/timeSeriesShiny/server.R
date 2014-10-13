library(shiny)
### Loading slow
ALLPRICE <- read.csv('./data/SPrice.csv')
ALLPROFILE <- read.csv('./data/SProfile.csv')

### find Developer's game

FINDDEVELOPERPROFILE <- function(developerName,queryFile=ALLPROFILE){
  developerFile <- queryFile[queryFile[,5]==developerName,]
  developerFile
}

##fine game price history
FINDDEVELOPERGAMEPRICELIST <- function(gameName,queryFile,queryPrice=ALLPRICE){
  gameID <- as.character(queryFile[which(queryFile[,2]==gameName),1])
  priceHistory <- queryPrice[which(queryPrice[,1]==gameID),3]
  priceHistory
}

DRAWCURVE <- function(priceHisory){
  priceTimeSeries <- ts(priceHisory)
  plot.ts(priceTimeSeries,col="red")
}

shinyServer(function(input, output, session) {
  output$control1 <- renderUI({
    selectInput("developerName", "Select Developer Name", choices = levels(ALLPROFILE[['developer']]))
  })
  
  output$control2 <- renderUI({
    x <- input$developerName
    if (any(
      is.null(x)
    ))
      return("Select")
    choice2 <-as.character(ALLPROFILE[which(ALLPROFILE[['developer']] == x),2])
    selectInput("gameName", "Select Game Name", choices = choice2)
  })
  
  output$plotTS <- renderPlot({
     developerFile<- FINDDEVELOPERPROFILE(input$developerName)
     priceHistory<- FINDDEVELOPERGAMEPRICELIST(input$gameName,developerFile)
     drawCurve<- DRAWCURVE(priceHistory)
     drawCurve
  })
  
})