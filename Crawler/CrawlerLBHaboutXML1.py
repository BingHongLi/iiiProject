#初版
#設定套件
import requests
from bs4 import BeautifulSoup
import HTMLParser
import urlparse
import time
import re
from math import ceil
'''test='http://store.steampowered.com/sub/17001/?snr=1_7_7_230_150_1'
category=re.search('(\w+):(...)(\w+).(\w+).(\w+).(\w+).(\w+)',test)
print category.group(6),category.group(7)
dataFormat='http://steamsales.rhekua.com/xml/sales/%s_%d.xml?curr=78'
print dataFormat%(category.group(6),int(category.group(7)))'''
success=0
fail=0
f=open('test2.txt')
for i in f.readlines():
    category=re.search('(\w+):(...)(\w+).(\w+).(\w+).(\w+).(\w+)',i)
    #tempFile='try/'+category.group(6)+'_'+category.group(7)+'.txt'
    #print tempFile
    rs=requests.session()
    if(category.group(6)=='video'):
        dataFormat='http://steamsales.rhekua.com/xml/sales/app_%d.xml?curr=78'
        response=rs.get(dataFormat%(int(category.group(7))))
        if(response.status_code!=404):
            tempFile='try/'+'app_'+category.group(7)+'.txt'
            content='content/'+'app_'+category.group(7)+'.txt'
            t=open(tempFile,'w')
            t.write(response.text)
            t.close()
            t=open(content,'w')
            temp2=rs.get(i).text.encode('utf8')
            t.write(temp2)
            t.close()
            success=success+1
        else:
            fail=fail+1
    else:
        dataFormat='http://steamsales.rhekua.com/xml/sales/%s_%d.xml?curr=78'
        response=rs.get(dataFormat%(category.group(6),int(category.group(7))))
        if(response.status_code!=404):
            tempFile='try/'+category.group(6)+'_'+category.group(7)+'.txt'
            content='content/'+category.group(6)+'_'+category.group(7)+'.txt'
            t=open(tempFile,'w')
            t.write(response.text)
            t.close()
            t=open(content,'w')
            temp2=rs.get(i).text.encode('utf8')
            t.write(temp2)
            t.close()
            success=success+1
        else:
            fail=fail+1    
    print tempFile
    print content
    print response.status_code
    print success,fail
f.close()
