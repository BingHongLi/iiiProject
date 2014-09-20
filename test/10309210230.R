#install package about text mining and twitter
#I will introduce text mining by using example about twitter
install.packages(c("tm","twitteR"))

#We will get a list after load rdmTweets.RData
load("D:/Dropbox/R/rdmTweets-201306.RData")

#show the data contents
tweets[1:3]

#將type為list的rdmTweets的每一筆資料轉成data.frame形式
#再採用列合併，一列即為一篇文章
df <- do.call('rbind',lapply(rdmTweets,as.data.frame))

#筆數、欄位
dim(df)

#使用tm包中的Corpus與VectorSource
#將所有文章拆成詞，轉作詞庫，
myCorpus <- Corpus(VectorSource(df$text))
