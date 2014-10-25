ORIGINDATA <- read.csv('E:/testLogistic2.csv')

View(ORIGINDATA)
colnames(ORIGINDATA) <- c("ID","COMPANY","YEAR","MONTH","DAY","WEEK","PRICE","HOLIDAY","PROMOTION")
ADJUSTDATA <- ORIGINDATA
#ADJUSTDATA['PRICE'] <-(ADJUSTDATA['PRICE']-min(ADJUSTDATA['PRICE']))/(max(ADJUSTDATA['PRICE']-min(ADJUSTDATA['PRICE'])))
View(ADJUSTDATA)

#log.glm <- glm(PROMOTION~YEAR+MONTH+DAY+WEEK+HOLIDAY,family=binomial,data=ADJUSTDATA)
log.glm <- glm(PROMOTION~HOLIDAY,family=binomial,data=ADJUSTDATA)
#possion.glm <- glm(PRICE~YEAR+MONTH+DAY+WEEK+HOLIDAY,family=poisson,data=ADJUSTDATA)

log.step <- step(log.glm)
summary(log.step)