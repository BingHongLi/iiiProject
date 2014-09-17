from bs4 import BeautifulSoup
import HTMLParser
f=open('app_10.txt','r')
t=f.readlines()
f.close()

x=""
for i in t:
    x+=i
#print x
content=BeautifulSoup(x)
#遊戲標題名
#print content.find('div',{'class':'apphub_AppName'}).text
#contentHeader=content.find('div',{'class':'apphub_AppName'}).text

#使用者認為的特性

'''chara=content.find('div',{'class':'glance_tags popular_tags'}).findAll('a')
for i in chara:
    #print i.text
    #print i.text.replace('\n','').replace('\t','')
    charaText=i.text.replace('\n','').replace('\t','')'''

#遊戲描述 建議使用第一個
#print content.find('div',{'id':'game_area_description'}).text.replace('\t','').replace('\n','') 
#print content.find('div',{'id':'game_area_description'}).text#.replace('\t','').replace('\n','')

#找出遊戲描述
'''for i in content.findAll('div',{'id':'game_area_description'}):
    print i.text'''

#找出系統需求
'''for i in content.findAll('div',{'id':'game_area_sys_req'}):
    print i.text'''

'''for i in range(len(content.findAll('div',{'id':'game_area_sys_req_full'}))):
    print content.findAll('div',{'id':'game_area_sys_req'})[i].find('h2').text.replace('\t','').replace('\n','').replace(' ','')
    print content.findAll('div',{'id':'game_area_sys_req_full'})[i].text.replace('\t','').replace('\n','')'''
#print content.find('div',{'id':'game_area_sys_req'}).find('h2').text.replace('\t','').replace('\n','')
#print content.find('div',{'id':'game_area_sys_req_full'}).text

#找出開發商的資訊、發售日、發行語言
#print content.find('div',{'class':'details_block'}).text
#print content.find('div',{'class':'details_block'})
#for a in content.find('div',{'class':'details_block'}).findAll('b')[1:5]:
#    print a.find('a').text
#    print a.text
'''print content.find('div',{'class':'details_block'}).text.replace('\t','').replace('\n','')
text = content.find('table',{'class':'game_language_options'}).findAll('tr')[1:]
for a in text:
    print a.text'''

#找出評論，未完成，網頁間id可能不同，不能套用
'''if content.find('div',{'id':'review_box partial'}) is None:
    print content.find('div',{'id':'Reviews_all'}).text'''