ORIGINDATA <- read.csv('SteamPrice16.csv',header=T,stringsAsFactors=F)

test <- ORIGINDATA[1,2:1000]
test <- test[!is.na(test)]
testTS <- ts(test,frequency=30)
testForecast <- HoltWinters(testTS,beta=F,gamma=F)
library(forecast)
testForecast20 <- forecast.HoltWinters(testForecast,h=20)
plot.forecast(testForecast20)
testForecast20
