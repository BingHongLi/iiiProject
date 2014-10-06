from bs4 import BeautifulSoup
import HTMLParser
import json
import os
import re

for dirPath, dirNames, AllfileNames in os.walk("C://Users/BigData/Desktop/sub/"):
    for fileName in AllfileNames:
        print fileName
        #print os.path.join(dirPath, f)
        a=re.search('(\w+)',fileName)
        ID=a.group(1)
        gameProfile={ID:{'ID':ID,'gameName':'','introduce':'','releaseDate':'',
                 'score':'','developer':'','publisher':'',
                 'systemRequire':''}}
        #讀檔案至暫存區，等待解析
        targetFilePath="C://Users/BigData/Desktop/sub/"+fileName
        of=open(targetFilePath,'r')
        t=of.readlines()
        of.close()
        x=""
        for i in t:
            x+=i
        #print x
        content=BeautifulSoup(x)

        #找出開發商、發行商、遊戲標籤、發售日
        #print content.find('div',{'class':'details_block'}).text

        con_list=str(content.find('div',{'class':'details_block'}))
        #print con_list
        split_list=con_list.split('<br>')
        #print split_list
      
        for event in split_list:
            #print event
            #print "-------------"
            event=event.replace('\n','')
            htmlevent=BeautifulSoup(event)
            
            #遊戲標籤
            if htmlevent.b is not None:
                if htmlevent.b.text == 'Genre:':
                    temp=htmlevent.findAll('a')
                    #for i in temp:
                    #print i.text
                #
                elif htmlevent.b.text == 'Title:':
                    temp=str(htmlevent)
                    gameProfile[ID]['gameName']=temp.split('<b>Title:</b>')[1].replace('\t','').replace('</p>','').replace('</div>','')
                #開發商
                elif htmlevent.b.text == 'Developer:':
                    temp=htmlevent.findAll('a')
                    tempDevelop=''
                    for i in temp:
                        #print i.text
                        tempDevelop+=i.text
                        #print tempDevelop 
                        gameProfile[ID]['developer']=tempDevelop
    
                #發行商
                elif htmlevent.b.text == 'Publisher:':
                    temp=htmlevent.findAll('a')
                    tempPublish=''
                    for i in temp:
                        #print i.text  
                        tempPublish+=i.text
                        gameProfile[ID]['publisher']=tempDevelop
                #發行日
                elif htmlevent.b.text == 'Release Date:':
                    temp=str(htmlevent)
                    gameProfile[ID]['releaseDate']=temp.split('<b>Release Date:</b>')[1].replace('\t','')
      

        gameProfileJson=json.dumps(gameProfile[ID], indent = 4)
        #print gameProfileJson
        targetFilePath='E://iiiProject/data/subContent/'+ID+'.json'
        print targetFilePath
        testFile=open(targetFilePath,'w')
        testFile.write(gameProfileJson)
        testFile.close()
        