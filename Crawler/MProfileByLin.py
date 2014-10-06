import requests
#這篇程式碼來自http://www.yihaomen.com/article/python/210.htm
#coding:utf-8
'''
Created on 2012-6-25
@author: lzs
''' 
# -*- coding: utf-8 -*-
import random
import socket
import urllib2
import cookielib

ERROR = {
        '0':'Can not open the url,checck you net',
        '1':'Creat download dir error',
        '2':'The image links is empty',
        '3':'Download faild',
        '4':'Build soup error,the html is empty',
        '5':'Can not save the image to your disk',
    }

class BrowserBase(object): 

    def __init__(self):
        socket.setdefaulttimeout(20)

    def speak(self,name,content):
        print '[%s]%s' %(name,content)

    def openurl(self,url):  
        """
        打开网页
        """
        cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
        urllib2.install_opener(self.opener)
        user_agents = [
                    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                    'Opera/9.25 (Windows NT 5.1; U; en)',
                    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",

                    ] 
       
         #模拟真实上网，发送了http header 的一些信息给appserver
        agent = random.choice(user_agents)
        self.opener.addheaders = [("User-agent",agent),("Accept","*/*"),('Referer','http://www.google.com')]
        try:
            res = self.opener.open(url)
            '''
            print res.read()
            '''            
        except Exception,e:
            self.speak(str(e)+url)
            raise Exception
        else:
            return res
'''        
# use class
if __name__=='__main__':
    splider=BrowserBase()
    splider.openurl('http://www.metacritic.com/browse/games/title/pc')    #取得網站資料
'''



#coding
from bs4 import BeautifulSoup
import time

def MetacriticCrawler(inputUrl):         #定義輸入method，輸出HTML
    if __name__=='__main__':        
        
        mGameName = inputUrl.split('/')[5]                                                                                                    #找出遊戲名稱
        print mGameName
        
        splider=BrowserBase()                                                                                                             #呼叫偽裝機器人                
        soup = BeautifulSoup(splider.openurl(inputUrl+'/details').read())                                           #抓下HTML
         
        
        
        print ('----------------------------------------------------------------------------------introduce--------------------------------------------------------------------------------------')
        #print soup.findAll('div',{"class":"summary_detail product_summary"})    
        if soup.findAll('div',{"class":"summary_detail product_summary"}):
            introduce=soup.findAll('div',{"class":"summary_detail product_summary"})                         #introduce  
            for i in introduce:
                print (' '.join(i.text.split())).split(':')[1]
        else:
            introduce=soup.findAll('li',{"class":"summary_detail product_summary"})                         #introduce  
            for i in introduce:
                print ' '.join(i.text.split(':'))
        
        print ('---------------------------------------------------------------------------------releaseDate------------------------------------------------------------------------------------')
        
        print ' '.join(soup.findAll('span',{"class":"data"})[1].text.split())                                        #releaseDate
        print ('----------------------------------------------------------------------------------metascore&userscore-------------------------------------------------------------------')    
        
        metascore = soup.find('div',{"class":"metascore_wrap feature_metascore"}).text.split()[1]               #metascore
        print (metascore)
        
        
        userscore = soup.find('div',{"class":"userscore_wrap feature_userscore"}).text.split()[2]                               #userscore
        print (userscore)
        

        '''
        f =open('MProfile.txt','a') 
        text ="text"
        f.write(text+"\n")
        f.close()
        '''
        
        
        
        print ('---------------------------------------------------------------------------developer & gameTag-----------------------------------------------------------------------------')    
        table = soup.find('table',{"cellspacing":"0"})                                                                                       #developer & gameTag
    
        gameTag=list()
        developer=list()
        for tag in table.findAll('tr'):                                                                                                      #逐一取出表格內容
            information = ''.join(tag.text.split())
            if information.split(':')[0] == 'Genre(s)' or information.split(':')[0] == 'ESRBDescriptors':
                gameTag.append(information.split(':')[1])
            if information.split(':')[0] == 'Developer':
                developer.append(information.split(':')[1])
        print gameTag[]
        print developer
        
        '''
        f =open('MGameTag.txt','a') 
        text ="text"
        f.write(text+"\n")
        f.close()
        '''
        print ('==================================================/critic-reviews-===========================================-')    
        #time.sleep()
        soup2 = BeautifulSoup(splider.openurl(inputUrl+'/critic-reviews').read())                                         #gameReview
        content = soup2.find('div',{"class":"body product_reviews"})
        
        i=0
        # help from 品中 取三標籤
        def match_class(target):                                                        
            def do_match(tag):                                                          
                classes = tag.get('class', [])                                          
                return all(c in classes for c in target)                                
            return do_match  
        '''
        f =open('MGameReview.txt','a') 
        text ="text"
        f.write(text+"\n")
        f.close()
        '''
        if content.find('div',{"class":"msg msg_no_reviews"}):
            print None
        else:    
            while content.find('div',{"class":"msg msg_no_reviews"}) is None:                                                                                                            #逐一取出內容
                if content.findAll('div',{"class":"date"}):
                    print content.findAll('div',{"class":"date"})[i].text
                if content.findAll('div',{'class':'source'}):
                    print content.findAll('div',{'class':'source'})[i].text
                if content.findAll('div',{'class':'review_body'}):
                    print ' '.join(content.findAll('div',{'class':'review_body'})[i].text.split())
                if content.findAll(match_class(["metascore_w", "medium", "game"])):                                                                  #取三個分數標籤
                    print content.findAll(match_class(["metascore_w", "medium", "game"]))[i].text
                i+=1
                
                if content.findAll('div',{"class":"review_body"}).__len__() == i:
                    break
#MetacriticCrawler method End
                
    
#a= 'http://www.metacritic.com/game/pc/1701-ad'
#MetacriticCrawler(a) 


    

f =open('MetaCritic_link_.txt','r')                         #open MetaCritic_link_.txt
index = f.readlines()
#print index.__len__()
for i in range(0,index.__len__()):
    link =index[i].split('|||||')[0].split('?full_summary=1')[0]
    MetacriticCrawler(link)    
f.close()













