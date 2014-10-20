library(shiny)
library(rpart.plot)
shinyUI(navbarPage("",
                   tabPanel("Price Trend",
                            sidebarLayout(
                                sidebarPanel(
                                    tabsetPanel("GameAnalysis",
                                                title="PriceTrend",
                                                type="pills",
                                                tabPanel(
                                                    uiOutput("control1")
                                                ),
                                                tabPanel(
                                                    uiOutput("control2")
                                                )                
                                    )
                                ),
                                mainPanel(
                                    plotOutput("plotTS")
                                )
                            )
                   ),tabPanel("Price Cluster",
                              sidebarLayout(
                                  sidebarPanel(
                                      tabsetPanel("GameAnalysis",
                                          title="PriceCluster",
                                          type="pills",
                                          tabPanel(
                                              uiOutput("control3")
                                          )
                                          ,
                                          tabPanel(
                                              uiOutput("control4")
                                          )
                                      )
                                  ),
                                  mainPanel(
                                      plotOutput("plotClusterTS")
                                  )
                              )
                   ), tabPanel("ClusterAnalysis",
                            sidebarLayout(
                                    sidebarPanel(
                                            tabsetPanel("ClusterAnalysis",
                                                  title="ClusterAnalysis",
                                                         type="pills",
                                                         tabPanel(
                                                            uiOutput("control5")
                                                         ),
                                                         tabPanel(
                                                            uiOutput("control6")
                                                         )    
                                                     )
                                                   ),
                                            mainPanel(
                                                   plotOutput("plotCluster")
                                                
                                            )
                             )
                                                 
                   ),
                   inverse = T, # ??????
                   theme=NULL # 設???css
                   #theme='test.css' 
)
)