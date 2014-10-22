# coding: utf-8

from BeautifulSoup import BeautifulSoup  
import os

source = 'E:\\python\\workspace\\SLanguagesETL\\res\\source'
target = 'E:\\python\\workspace\\SLanguagesETL\\res\\target'
#source = 'D:\\YB802\\python\\workspace\\SLanguagesETL\\res\\source' 
#target = 'D:\\YB802\\python\\workspace\\SLanguagesETL\\res\\target'

#Get title from title.txt
title_file = open(target + '\\' + 'title.txt', 'r')
title = title_file.readline().decode('utf-8')
title_file.close()
fields = title.split(',')[1:]

#Create error_file
error = open(target + '\\' + 'error_bool.txt', 'w')
tar_file = open(target + '\\' + 'SLanguages.csv', 'w')
tar_file.write(title + '\n')

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
            record = ['0'] * len(fields)            
            for tr in lang_table.findAll('tr')[1:]:
                #Catch if the language is supported
                lang_sup = tr.find('td', {'class': 'checkcol'})
                #Catch the language supported in interface
                if lang_sup and lang_sup.find('img') is not None:
                    lang = tr.find('td', {'class': 'ellipsis'}).text.encode('utf-8').strip().lower()
                    #Change tchinese old form to new one 
                    lang = lang.replace('tchinese', 'traditional chinese')
                    #Catch the language in the fields
                    for language in fields:
                        if lang.find(language) != -1:
                            record[fields.index(language)] = '1'                            
            output = f.split('.')[0] + ',' + ','.join(record)         
            tar_file.write(output + '\n')        
        else:
            error.write(f.encode('utf-8') + '\n')
            
        print f 
            
error.close()
tar_file.close()
