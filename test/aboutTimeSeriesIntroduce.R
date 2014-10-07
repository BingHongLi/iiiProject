###基本單維時間序列
#讀取資料，並忽略文件前三行
kings <- scan("http://robjhyndman.com/tsdldata/misc/kings.dat",skip=3)
#將資料讀進時間序列中
kingsTimeSeries <- ts(kings)
#繪製英國國王(依序)去世年齡序列圖
plot.ts(kingsTimeSeries)

#讀取1946年1月-1959年12月紐約每月出生人口數
births <- scan('http://robjhyndman.com/tsdldata/data/nybirths.dat')
#資料時間序列化
birthsTimeSeries <- ts(births,,frequency=12,start=c(1946,1))
#畫一個紐約每月出生人口數量的時間序列圖
plot.ts(birthsTimeSeries)

#讀取1987年1月-1987年12月的每月銷售數據，並時間序列化
souvenir <- scan('http://robjhyndman.com/tsdldata/data/fancy.dat')
souvenirTimeSeries <- ts(souvenir,start=c(1987,1),frequency=12)
#繪圖，發現季節性波動和隨機變動的大小是隨時間序列逐步上升
plot.ts(souvenirTimeSeries)
#取自然對數進行轉換計算，並繪圖
logSouvenirTimeSeries <- log(souvenirTimeSeries)
plot.ts(logSouvenirTimeSeries)

### 分解時間序列
## 分解時間序列，一般分為趨勢部分，一個不規則部分，若為季節性時間序列，則還有一個季節性部分

## 分解非季節性數據
# 須估計趨勢與不規則的兩部分
# 為估計非季節性時間序列的趨勢，使之能用相加模型，最常見的方法為平滑法，比如計算時間序列的簡單移動平均
# TTR包可使用簡單的移動平均來平滑時間序列
library(TTR)
# 使用SMA()函數時，需輸入參數n指定簡單移動平均的跨度
# 國王去世資料呈現出非季節性，並且隨機變動在整個時段內大致不變
# 固可當作一個相加模型。
# 使用簡單移動平均平滑來估計國王去世的趨勢部分
kingsTimeSeriesSMA3 <- SMA(kingsTimeSeries,n=3)
plot.ts(kingsTimeSeriesSMA3)
# 可從圖上看出時間序列仍呈現出大量隨便波動，因此需嘗試更大的跨度進行平滑
kingsTimeSeriesSMA8 <- SMA(kingsTimeSeries,n=8)
plot.ts(kingsTimeSeriesSMA8)
#可從圖上看出更為平滑，時間序列前20位國王去世年齡從55歲下降至38歲，然後上升至第40位國王的73歲

## 分解季節性數據
# 一個季節性序列包含一個趨勢部分、季節性部分和不規則部分
# 分解季節性，就意味著要把時間序列分解為這三個部分，也就是估計出這三個部分
# 對於可使用相加模型進行描述的趨勢部分與季節性部分，可使用decompose()函數來估計
# decompose 可估出時間序列中趨勢、季節和不規則的部分，而此時間序列是可用相加模型描述的
# decompose 回傳一個list，裡面包含了季節性部分(seasonal)、趨勢部分(trend)和不規則部分(random)
# 若季節性變動與隨機變動在時間段內大致不變，則此模型很有可能是可用相加模型來描述

# 剖析紐約出生人數
birthTimeSeriesComponents <- decompose(birthsTimeSeries)

# 去除季節性部分不看
birthsTimeSeriesSeasonallyAdjusted <- birthsTimeSeries - birthTimeSeriesComponents$seasonal
plot(birthsTimeSeriesSeasonallyAdjusted)


### 使用指數平滑法進行預測─用於時間序列的短期預測

## 簡單指數平滑法
# 適用在可相加模型且恆定水平及沒有季節性變動的時間序列
# 提供alpha參數來控制平滑，alpha介於0到1之間，alpha越接近0的時候，
# 鄰近預測的觀測值在預測中的權重就越小
rain <- scan('http://robjhyndman.com/tsdldata/hurst/precip1.dat',skip=1)
rainSeries <- ts(rain,start=c(1813))
plot.ts(rainSeries)

# 從圖知曲線處於大致不變的水平，可被描述成一個相加模型
# 使用簡單指數平滑法預測
rainSeriesForeasts <- HoltWinters(rainSeries,beta=F,gamma=F)

# HoltWinters()產生的預測存儲在rainSeriesForeasts的list內變量名為fitted
rainSeriesForeasts$fitted
plot(rainSeriesForeasts)

# 作為預測準確度的一個度量，可計算樣本內預測誤差的誤差平方和，結果存在list的SSE變量
rainSeriesForeasts$SSE

# 若想改初始水平，代碼如下
HoltWinters(rainSeries,beta=F,gamma=F,l.start=23.56)

# HoltWinters僅僅是預測時期即覆蓋原始數據的時期，可改用foreast包中的forecast.HoltWinters()進行更遠時間點上的預測
library(forecast)

# forecast.HoltWinters()函數，第一個參數input,可在已使用HoltWinters()函數調整後的預測模型中忽略它
# 裡面有一參數h，用來制定想要做多少時間點的預測
rainSeriesForeasts2 <- forecast.HoltWinters(rainSeriesForeasts,h=8)
rainSeriesForeasts2

# 繪製預測圖，中間為80%的預測區間，上下兩方為95%的預測區間
plot.forecast(rainSeriesForeasts2)

# 使用forecast.HoltWinters()返回的樣本內預測誤差將被存儲在list內的residual變量中，
# 如果預測模型不可再被優化，連續預測中的預測誤差是不相關的，若為相關的，很有可能簡單指數平滑可被另一種預測技術優化
# 為了驗證，需去獲取樣本誤差中1-20階的相關圖，可通過acf()函數計算預測誤差的相關圖
# 為了指定我們想要看到的最大階數，可使用acf()中的lag.max參數

# 計算倫敦降雨量數據的樣本內預測誤差延遲1-20階的相關圖
acf(rainSeriesForeasts2$residuals,lag.max=20)

# 讀至p.24頁
