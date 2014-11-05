# coding: utf-8

from BeautifulSoup import BeautifulSoup  
import os,re

source = 'E:\\python\\workspace\\SLanguagesETL\\res\\source'
target = 'E:\\python\\workspace\\SLanguagesETL\\res\\target'
#source = 'D:\\YB802\\python\\workspace\\SLanguagesETL\\res\\source' 
#target = 'D:\\YB802\\python\\workspace\\SLanguagesETL\\res\\target'
header = 'ID,languages' + '\n'
plate =re.compile('[a-z \-]+')
languages = set()

#Create error_file
error = open(target + '\\' + 'error_file.txt', 'w')

#Read each file
for root, dirs, files in os.walk(source):       
    for f in files:
        src = os.path.join(root, f)
        
#Catch file content.      
        src_file = open(src, 'r')
#src_file = open(source + '\\' + 'allContentUSA' + '\\' + 'app_10600.txt', 'r')
        src_text = src_file.read().decode('utf-8')
        src_file.close()

#Catch languages table        
        src_soup = BeautifulSoup(''.join(src_text))
        lang_table = src_soup.find('table', {'class': 'game_language_options'})
            
#Catch each row
        if lang_table is not None:
            for tr in lang_table.findAll('tr')[1:]:
                #Catch if the language is supported
                lang_sup = tr.find('td', {'class': 'checkcol'})
                #Catch the language supported in interface
                if lang_sup and lang_sup.find('img') is not None:
                    lang = tr.find('td', {'class': 'ellipsis'}).text.encode('utf-8').strip().lower()
                    m = plate.match(lang)
                    if m is not None:
                        languages.add(m.group())
            print f
        else:
            error.write(f.encode('utf-8') + '\n')

error.close()
        
#tar_file = open(target + '\\' + 'allLanguages.txt', 'w')
output = 'ID,' + ','.join(languages)
print output

tar_file = open(target + '\\' + 'title.txt', 'w')
tar_file.write(output)
tar_file.close()