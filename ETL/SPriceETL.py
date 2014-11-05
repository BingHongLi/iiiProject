# coding: utf-8

from BeautifulSoup import BeautifulSoup  
import os

source = 'E:\\python\\workspace\\SPriceETL\\res\\source'
target = 'E:\\python\\workspace\\SPriceETL\\res\\target'
#source = 'D:\\YB802\\python\\workspace\\SPriceETL\\res\\source' 
#target = 'D:\\YB802\\python\\workspace\\SPriceETL\\res\\target'
header = 'ID,recordTime,recordPrice' + '\n'

#Create target the file
tar_file = open(target + '\\' + 'SPrice.csv', 'w')
tar_file.write(header.encode('utf-8'))

#Read each file
for root, dirs, files in os.walk(source):   
    for f in files:
        src = os.path.join(root, f)
        src_file = open(src, 'r')
        
        #Catch all content of the file
        src_text = src_file.read().decode('utf-8')
        src_file.close()
        
        ID = f.split('.')[0]
        src_soup = BeautifulSoup(''.join(src_text))
        for record in src_soup.findAll('set'):
            recordTime = record['name']
            recordPrice = record['value']
            output ='\"' + ID + '\"'  + ',' + '\"' + recordTime + '\"' + ',' + '\"' + recordPrice + '\"' + '\n'
            
            tar_file.write(output.encode('utf-8'))
        print src
            
tar_file.close()        
    