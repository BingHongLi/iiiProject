__author__ = 'bigdata'
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
#import time
import sys

reload(sys)
sys.setdefaultencoding('utf8') #change encode


def MetacriticCrawler(inputUrl):         #定義輸入method，輸出HTML
    if __name__=='__main__':

        mGameName = inputUrl.split('.')[0]                                                                                                    #找出遊戲名稱
        #print mGameName
        path ="/home/bigdata/IdeaProjects/Metacritic/details/"+inputUrl

        f =open(path,"r")
        #b= f.read().encode('utf8')
        b= f.read()

        soup = BeautifulSoup(b)                                        #抓下HTML
        f.close()


        othername =''
        f =open('MetaCritic_link_.txt','r')                         #open MetaCritic_link_.txt
        index = f.readlines()
        #print index.__len__()
        for i in range(0,index.__len__()):

            link =index[i].split('|||||')[0].split('?full_summary=1')[0]
            if link.split('/')[5] ==mGameName:
                othername= index[i].split('|||||')[1].split()[0]
                break
        f.close()
        print othername


        MProfile={'MGameName':mGameName,'SteamGamename':othername,'Introduce':'','ReleaseDate':'','MetaScore':'','UserScore':'','Developer':''}


        #print soup.findAll('div',{"class":"summary_detail product_summary"})
        if soup.findAll('div',{"class":"summary_detail product_summary"}):
            introduce=soup.findAll('div',{"class":"summary_detail product_summary"})                         #introduce
            for i in introduce:
                point = (' '.join(i.text.encode('utf-8').split())).split(':')[1].replace('â','-').replace('â','\'')
                MProfile['Introduce'] = point
        else:
            introduce=soup.findAll('li',{"class":"summary_detail product_summary"})         #introduce
            for i in introduce:
                point = ' '.join(i.text.split(':')).replace('â','-').replace('â','\'')
                MProfile['Introduce'] = point

        #print ('---------------------------------------------------------------------------------releaseDate------------------------------------------------------------------------------------')
        point = ' '.join(soup.find('li',{"class":"summary_detail release_data"}).find('span',{"class":"data"}).text.split())                                #releaseDate
        MProfile['ReleaseDate'] = point                                                                                     #releaseDate
        #print ('----------------------------------------------------------------------------------metascore&userscore-------------------------------------------------------------------')

        metascore = soup.find('div',{"class":"metascore_wrap feature_metascore"}).text.encode('utf-8').split()[1]               #metascore
        userscore = soup.find('div',{"class":"userscore_wrap feature_userscore"}).text.encode('utf-8').split()[2]                               #userscore
        if metascore != 'tbd' and userscore != 'tbd':
            MProfile['MetaScore'] =metascore
            MProfile['UserScore'] =userscore


        #print ('---------------------------------------------------------------------------developer & gameTag-----------------------------------------------------------------------------')
        MGameTag={'MGameName':mGameName,'SteamGamename':othername,'GameTag':''}


        if soup.find('table',{"cellspacing":"0"}) :
            table = soup.find('table',{"cellspacing":"0"})                                                                                       #developer & gameTag

            gameTag=list()
            developer=list()
            for tag in table.findAll('tr'):                                                                                                      #逐一取出表格內容
                information = ''.join(tag.text.encode('utf-8').split())
                if information.split(':')[0] == 'Genre(s)' or information.split(':')[0] == 'ESRBDescriptors':
                    gameTag.append(information.split(':')[1])
                if information.split(':')[0] == 'Developer':
                    developer.append(information.split(':')[1])
            for i in range(0,developer.__len__()):
                MProfile['Developer']=(developer[i])
            for i in range(0,gameTag.__len__()):
                MGameTag['GameTag'] = gameTag[i]
        #print '++++'
        #print MProfile['Introduce']


        f =open('MProfile3.txt','a')
        f.write('\"'+MProfile['MGameName']+'\"|\"'+MProfile['SteamGamename']+'\"|\"'+MProfile['Developer']+'\"|')
        f.write('\"'+MProfile['ReleaseDate']+'\"|\"'+MProfile['MetaScore']+'\"|\"'+MProfile['UserScore']+'\"|\"'+MProfile['Introduce']+'\"')
        f.write("\n")
        f.close()


        #print ('-------------------------------------------------------------------------MGameName,SteamGamename,GameTag--------------------------------------------------')

        #print gameTag

        f =open('MGameTag3.txt','a')
        f.write('\"'+MGameTag['MGameName']+'\"|\"'+MGameTag['SteamGamename']+'\"|\"'+ MGameTag['GameTag']+'\"')
        f.write("\n")
        f.close()



        #print ('==================================================/critic-reviews-===========================================-')
        #time.sleep()
        path ="/home/bigdata/IdeaProjects/Metacritic/critic-reviews/"+inputUrl
        f =open(path,"r")
        c= f.read()#.encode('utf8')
        soup2 = BeautifulSoup(c)                                        #抓下HTML
        f.close()                                                                                                             #gameReview



        MGameReview={'MGameName':mGameName,'SteamGamename':othername,'GameReview':'','Date':'','Score':'','Writer':''}

        # help from 品中 取三標籤
        def match_class(target):
            def do_match(tag):
                classes = tag.get('class', [])
                return all(c in classes for c in target)
            return do_match

        '''
        content = soup2.find('div',{"class":"body product_reviews"})
        f =open('MGameReview3.txt','a')
        while content.find('div',{"class":"msg msg_no_reviews"}) is None:                                                                                                            #逐一取出內容
            if content.findAll('div',{"class":"date"})[i] is True:
                #print content.findAll('div',{"class":"date"})[0].text.encode('utf-8').split()
                Date = content.findAll('div',{"class":"date"})[i].text.encode('utf-8').split()
                MGameReview['Date'] =' '.join(Date)
                #print Date
            if content.findAll('div',{'class':'source'}):
                Writer = content.findAll('div',{'class':'source'})[i].text.encode('utf-8').split()[0]
                MGameReview['Writer'] = Writer
                #print Writer
            if content.findAll('div',{'class':'review_body'}):
                GameReview = ' '.join(content.findAll('div',{'class':'review_body'})[i].text.encode('utf-8').split()).replace('â','-').replace('â','\'')
                MGameReview['GameReview'] =GameReview
                #print GameReview

            if content.findAll(match_class(["metascore_w", "medium", "game"])):                                                                  #取三個分數標籤
                Score = content.findAll(match_class(["metascore_w", "medium", "game"]))[i].text.encode('utf-8').split()[0]
                MGameReview['Score'] =Score
                #print Score
            #print MGameReview



            f.write('\"'+MGameReview['MGameName']+'\"|\"'+MGameReview['SteamGamename']+'\"|\"'+MGameReview['Writer']+'\"|')
            f.write('\"'+MGameReview['Date']+'\"|\"'+MGameReview['Score']+'\"|\"'+MGameReview['GameReview']+'\"')
            f.write("\n")

            i+=1

            if content.findAll('div',{"class":"review_body"}).__len__() == i:
                f.close()
                break
        '''

        i=0
        f =open('MGameReview3.txt','a')
        if soup2.find('div',{"class":"body product_reviews"}).find('div',{"class":"msg msg_no_reviews"}) is None:
            content =soup2.findAll('div',{"class":"review_btm review_btm_r"})
            while soup2.find('div',{"class":"body product_reviews"}).find('div',{"class":"msg msg_no_reviews"}) is None:                                                                                                            #逐一取出內容
                if content[i].find('div',{"class":"date"}):
                    #print content[i].find('div',{"class":"date"}).text.encode('utf-8').split()
                    Date = content[i].find('div',{"class":"date"}).text.encode('utf-8').split()
                    MGameReview['Date'] =' '.join(Date)
                    #print Date
                if content[i].find('div',{'class':'source'}):
                    Writer = ' '.join(content[i].find('div',{'class':'source'}).text.encode('utf-8').split())
                    MGameReview['Writer'] = Writer
                #print Writer
                if content[i].find('div',{'class':'review_body'}):
                    GameReview = ' '.join(content[i].find('div',{'class':'review_body'}).text.encode('utf-8').split()).replace('â','-').replace('â','\'')
                    MGameReview['GameReview'] =GameReview
                    #print GameReview

                if content[i].find(match_class(["metascore_w", "medium", "game"])):                                                                  #取三個分數標籤
                    Score = content[i].find(match_class(["metascore_w", "medium", "game"])).text.encode('utf-8').split()[0]
                    MGameReview['Score'] =Score
                #print Score
            #print MGameReview



                f.write('\"'+MGameReview['MGameName']+'\"|\"'+MGameReview['SteamGamename']+'\"|\"'+MGameReview['Writer']+'\"|')
                f.write('\"'+MGameReview['Date']+'\"|\"'+MGameReview['Score']+'\"|\"'+MGameReview['GameReview']+'\"')
                f.write("\n")
                MGameReview={'MGameName':mGameName,'SteamGamename':othername,'GameReview':'','Date':'','Score':'','Writer':''}

                i+=1

                if soup2.find('div',{"class":"body product_reviews"}).findAll('div',{"class":"review_body"}).__len__() == i:
                    f.close()
                    break



#MetacriticCrawler method End


#a= 'http://www.metacritic.com/game/pc/1701-ad'
#MetacriticCrawler('king-arthur-the-role-playing-wargame.txt')



import os
for dirPath, dirNames, fileNames in os.walk("/home/bigdata/IdeaProjects/Metacritic/details/"):
    for fileName in fileNames:
        print fileName
        MetacriticCrawler(fileName)





