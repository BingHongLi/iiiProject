#-*- coding: utf-8 -*-
import re
import time
import json
import requests
from BeautifulSoup import BeautifulSoup
import csv
def select_script_text(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode('utf-8'))
    search_name = soup.findAll('div',{'class' : 'cntBoxTitle'})[1].text.replace('Price History: ', '')
    search_script_text = soup.find('script', {'type' : 'text/javascript'}).text
    cols = re.search(r'cols:.*}}],',search_script_text)
    rows = re.search(r'rows:.*}]}]',search_script_text)
    return (cols.group(), rows.group(), search_name)
   
def isthereanydeal_history_ajaxs(input_file, output_folder):
    http_link = 'http://isthereanydeal.com/ajax/game/price?plain=' + input_file
    script_text = select_script_text(http_link)

    col = script_text[0]
    row = script_text[1]
    game_name = script_text[2]
    
    m = re.findall('label:\'[a-zA-Z ]+\'', col)[1:]
    company = [temp.replace('label:', '').replace('\'', '') for temp in m]
   
    special_time = []
    for temp_t in re.findall('(v:new Date\(\d{10})', row):
        temp_t = int(temp_t.replace(r'v:new Date(',''))
        special_time.append(time.strftime('%Y-%m-%d %H:%M', time.gmtime(int(temp_t))))

    special_time_day = re.split(r',?c:\[v\:new Date\(\d{13}\)\,', \
                                row[8:].replace(']', '').replace('{', '').replace('}', ''))[1:]
    special_time_company = [re.findall('(v:null|v:[0-9\.]+),(v:false|v:true),(v:false|v:true)', special_company)\
                            for special_company in special_time_day]
    special_day = []
    special_days = {}
 
    for i in range(len(company)):
        for j in range(len(special_time)):
            #if special_time_company[i][j][0] == 'v:null':
            #    continue
            special_days['company'] = company[i]
            special_days['date'] = special_time[j]
            special_days['price'] = special_time_company[j][i][0].replace('v:', '')
            special_days['price_have_special_before'] = special_time_company[j][i][1].replace('v:', '')
            special_days['price_special'] = special_time_company[j][i][2].replace('v:', '')
            special_day.append(special_days.copy())
    change_to_json = json.dumps(special_day, ensure_ascii=False, sort_keys=True)
    #change_to_json = json.dumps(special_day, ensure_ascii=False, sort_keys=True, indent=4)

    with open(output_folder + input_file + '_company.json', 'a') as file_W:
        file_W.write(change_to_json.encode('utf8'))
        
def main():
    isthereanydeal_history_ajaxs('findingteddy', 'C:/Users/BigData/Desktop/')

if __name__ == "__main__":
    main()

