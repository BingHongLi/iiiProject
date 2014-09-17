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
#使用者認為的特性
'''chara=content.find('div',{'class':'glance_tags popular_tags'}).findAll('a')
for i in chara:
    print i.text'''

#遊戲描述
#print content.find('div',{'id':'game_area_description'}).text

#找出遊戲描述
'''for i in content.findAll('div',{'id':'game_area_description'}):
    print i.text'''

#找出系統需求
'''for i in content.findAll('div',{'id':'game_area_sys_req'}):
    print i.text'''

#找出開發商的資訊、發售日、發行語言
#print content.find('div',{'class':'details_block'}).text

#找出評論，未完成，網頁間id可能不同，不能套用
'''if content.find('div',{'id':'review_box partial'}) is None:
    print content.find('div',{'id':'Reviews_all'}).text'''
