#-*- coding: utf-8 -*-
import re
import time
import json

def isthereanydeal_history_ajaxs(input_file, output_folder):
    file_R = open(input_file, 'r')
    rows = file_R.readlines()
    file_R.close()

    row_3 = rows[3]
    row_4 = rows[4]

    #刪除第一個id:'date'
    m = re.findall('id:\'\w*\'', rows[3])[1:]
    #取出賣場名稱
    company = [temp.replace('id:', '').replace('\'', '') for temp in m]

    #取出時間, 將毫秒轉換為日期
    #special_time_raw = [int(temp_t.replace(r'v:new Date(','')) for temp_t in re.findall('(v:new Date\(\d{10})', rows[4])]
    #special_time = [time.strftime('%Y-%m-%d', time.gmtime(int(temp_t))) for temp_t in special_time_raw]
    special_time = []
    for temp_t in re.findall('(v:new Date\(\d{10})', rows[4]):
        temp_t = int(temp_t.replace(r'v:new Date(',''))
        special_time.append(time.strftime('%Y-%m-%d', time.gmtime(int(temp_t))))

    #以',c:[v:new Date(d{13}),'截字串, 並刪除{ } ]
    special_time_day = re.split(r',?c:\[v\:new Date\(\d{13}\)\,', \
                                rows[4].replace(']', '').replace('{', '').replace('}', '').lstrip()[7:])[1:]

    #取出各公司販售價格, null為未販售
    special_time_company = [re.findall('(v:null|v:[0-9\.]+),(v:false|v:true),(v:false|v:true)', special_company)\
                            for special_company in special_time_day]
    #special_time_company[i][j][0] 為有無販售

    special_days = {}
    for i in range(len(special_time)):
        special_day = {}
        for j in range(len(company)):
            #if special_time_company[i][j][0] == 'v:null':
            #    continue
            special_day[company[j]] = special_time_company[i][j]
        special_days[special_time[i]] =  special_day

    #轉為json 參閱http://liuzhijun.iteye.com/blog/1859857    
    change_to_json = json.dumps(special_days, ensure_ascii=False, sort_keys=True, indent=4)
    with open(output_folder + 'findingteddy_no_indent.json', 'w') as file_W:
        file_W.write(change_to_json)

crawler_steam_pages_links('C:/Users/BigData/Desktop/findingteddy_ajax.txt'\
                          , 'C:/Users/BigData/Desktop/')
