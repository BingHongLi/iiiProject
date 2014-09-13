'''
以先前的CrawlerLBH1 抓取steam臺灣區所有連結
而後進行抓取金額XML的動作，而後按照種類及編號存成檔案
並計算成功數量與失敗數量
尚有精進的空間，如video歸類成sub或app的部分。
'''
#設定計數器
success=0
fail=0
#讀取連結檔案
f=open('test3.txt','r')
#針對每一行連結進行如下動作
for i in f.readlines():
	#正規表示法取得編號
    category=re.search('(\w+):(...)(\w+).(\w+).(\w+).(\w+).(\w+)',i)
    #組成儲存路徑及檔案名
	tempFile='try/'+category.group(6)+'_'+category.group(7)+'.txt'
    #print tempFile
    rs=requests.session()
	#進行辨認，如果取得字串為video，將轉成app，進行讀取，但video仍有可能為sub或其他，故仍有404的發生可能
    if(category.group(6)=='video'):
        dataFormat='http://steamsales.rhekua.com/xml/sales/app_%d.xml?curr=78'
        rs=requests.session()
        response=rs.get(dataFormat%(int(category.group(7))))
		#若沒發生404，則進行建檔的動作
        if(response.status_code!=404):
            t=open(tempFile,'w')
            t.write(response.text)
            t.close()
            success=success+1
        else:
            fail=fail+1
	#取得字串非video，進行如下動作。
    else:
        dataFormat='http://steamsales.rhekua.com/xml/sales/%s_%d.xml?curr=78'
        response=rs.get(dataFormat%(category.group(6),int(category.group(7))))
        if(response.status_code!=404):
            t=open(tempFile,'w')
            t.write(response.text)
            t.close()
            success=success+1
        else:
            fail=fail+1    
    print tempFile
    print response.status_code
    print success,fail
#關閉檔案串流
f.close()