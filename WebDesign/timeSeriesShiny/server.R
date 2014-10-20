library(shiny)
library(rpart.plot)
### Loading slow
ALLPRICE <- read.csv('./data/SPrice.csv')
ALLPROFILE <- read.csv('./data/SProfile.csv')
CLUSTERPRICE = readRDS('./data/allPrice.RDS')
CLUSTER_1496 = read.csv('./data/CLUSTER_1496.csv')
ALLCLUSTER <- read.csv('./data/ClusterClassifier.csv')

### find Developer's game
FINDDEVELOPERPROFILE <- function(developerName,queryFile=ALLPROFILE){
  developerFile <- queryFile[queryFile[,5]==developerName,]
  developerFile
}

### fine game price history
FINDDEVELOPERGAMEPRICELIST <- function(gameName,queryFile,queryPrice=ALLPRICE){
  gameID <- as.character(queryFile[which(queryFile[,2]==gameName),1])
  priceHistory <- queryPrice[which(queryPrice[,1]==gameID),3]
  priceHistory
}

### Draw Curve
DRAWCURVE <- function(priceHistory){
  # TimeSerise Data
  priceTimeSeries <- ts(priceHistory)
  # Draw curve
  plot.ts(priceTimeSeries,col="red")
  
}

### Cluster Compare return a rpart's list
CLUSTERCOMPARE <- function(cluster1,cluster2){
  
  C1<- ALLCLUSTER[which(ALLCLUSTER[,3]==cluster1),]
  C2<- ALLCLUSTER[which(ALLCLUSTER[,3]==cluster2),]
  ALLCLUSTERATTR <- rbind(C1,C2)
  myFomula <- CLARA~Accounting+Adventure+Casual+Education+Indie+Racing+RPG
  test_rpart <- rpart(myFomula,method="class",data=ALLCLUSTERATTR,control=rpart.control(minsplit=10))
  #plot(test_rpart)
  #text(test_rpart,use.n = TRUE, all=T)
  #rpart.plot(test_rpart)
}



shinyServer(function(input, output, session) {
  
  #############For control  ##########
  
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
  
  output$control3 <- renderUI({
    selectInput("clusterName", "Select cluster Name", choices = as.character(c(1:20)))
  })
  
  output$control4 <- renderUI({
    xx <- input$clusterName
    if (any(
      is.null(xx)
    ))
      return("Select")
    selectInput("clusterGameName", "Select Game Name", choices = as.character(CLUSTER_1496['X'][,1][which(CLUSTER_1496['clara']== as.numeric(xx))]))
  })
  
  output$control5 <- renderUI({
    selectInput("clusterNumber1", "Select Cluster Number", choices =c(1:20),selected=1 )
  })
  
  output$control6 <- renderUI({
    selectInput("clusterNumber2", "Select other Cluster Number ", choices = c(1:20),selected=2)
  })
  
  #############For plot  ############
  
  ### find Developer's game and draw curve
  output$plotTS <- renderPlot({
    # generate develper's profile
    developerFile<- FINDDEVELOPERPROFILE(input$developerName)
    
    # generate gamePrice's list
    priceHistory<- FINDDEVELOPERGAMEPRICELIST(input$gameName,developerFile)
    
    # draw
    drawCurve<- DRAWCURVE(priceHistory)
    drawCurve
  })
  
  ### depend on your choice cluster and draw curve
  output$plotClusterTS <- renderPlot({
    drawCurve <- DRAWCURVE(CLUSTERPRICE[[input$clusterGameName]])
    drawCurve
  })
  
  ### draw decision tree
  output$plotCluster <- renderPlot({
    rpart.plot(CLUSTERCOMPARE(input$clusterNumber1,input$clusterNumber2))
  })
  
  
})