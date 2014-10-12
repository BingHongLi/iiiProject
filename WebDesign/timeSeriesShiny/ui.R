library(shiny)
allDevelopName <- read.csv('./Data/allDeveloperName.csv',header=F)

shinyUI(fluidPage(
  title="GameAnalysis",
  titlePanel("GameTrendAnalysis"),
  fluidRow(
    column(4,
           tabsetPanel(
             title="PriceTrend",
             type="pills",
             tabPanel(  
               selectInput("selectDeveloper","Select Developer", choices=levels(allDevelopName[,1]))
             ),
             tabPanel(  
               selectInput("selectGames","Select Game", choices=c("app_102820","app_102822","app_47790"))
             )
           )
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("PlotTS",plotOutput("plotTS"))
      )
    )
    
  )
  
))