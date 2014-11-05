# coding: utf-8

from BeautifulSoup import BeautifulSoup  
import os

source = 'E:\\python\\workspace\\MetacriticCrawler\\res'
target = 'E:\\python\\workspace\\MUsersReviewsETL\\res'
#source = 'D:\\YB802\\python\\workspace\\MetacriticCrawler\\res' 
#target = 'D:\\YB802\\python\\workspace\\MUsersReviewsETL\\res'
header = 'mGameName,userReviewTime,userScore,userReview' + '\n'

#Create target file
tar_file = open(target + '\\' + 'MusersReviews.csv', 'w')
tar_file.write(header.encode('utf-8'))

#Read each file
for root, dirs, files in os.walk(source + '\\' + 'user-reviews'):       
    for f in files:               
        src_file = open(root + '\\' + f, 'r')

#Catch all content of the file
        src_text = src_file.read().decode('utf-8')
        src_file.close()

#Catch the fields
        src_soup = BeautifulSoup(''.join(src_text))
        mGameName = src_soup.find('a', {'class' : 'hover_none'}).text.strip()

#Catch the fields in each comment.
        if src_soup.find('div', {'class': 'review_section'}) is not None:
            
            for rev_block in src_soup.findAll('div', {'class': 'review_section'}):
                
                userScore = rev_block.find('div', {'class': 'review_grade'}).text.strip()        
                userReviewTime = rev_block.find('div', {'class': 'date'}).text.strip()                   
                userReview = rev_block.find('div', {'class': 'review_body'}).text
                #Deal the expanded and collapsed    
                review_e = rev_block.find('span', {'class': 'blurb blurb_expanded'})
                if review_e is not None:
                    review_c = rev_block.find('span', {'class': 'blurb blurb_collapsed'})
                    userReview = review_c.text + ' ' + review_e.text
                    
                #Replace '"' by "'", line feed by ' ' in comment
                userReview = userReview.strip().replace('\"', "\'").replace('\n', ' ').replace('\r', ' ')
            
                #Construction of an record    
                record = '\"' + mGameName + '\"' + ',' + '\"' + userReviewTime + '\"' + ',' + '\"' + userScore + '\"' + ',' + '\"' + userReview + '\"' + '\n'
        
                tar_file.write(record.encode('utf-8'))
            print f
    
tar_file.close()