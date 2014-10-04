#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

def game_info_ajaxs(input_name, output_folder):
    link = 'http://isthereanydeal.com/ajax/game/info?plain={0}'.format(input_name)
    res = requests.get(link)
    soup = BeautifulSoup(res.text.encode('utf-8'))

    game_info = soup.find_all('div', {'class' : 'link'})[1]

    if game_info.text == 'You can try your luck searching by yourself, though.':
        with open(output_folder + 'mabey_null.txt', 'a') as file_maybe_null:
            file_maybe_null.write(link + ' |||| ' + soup.find('div', {'id':'pageContent'}).h2.text + '\n')
    elif re.compile (r'MetaCritic.com'):
        with open(output_folder + 'MetaCritic_link.txt', 'a') as file_MetaCritic_link:
            file_MetaCritic_link.write(game_info.a['href'] + ' |||| ' + soup.find('div', {'id':'pageContent'}).h2.text  + '\n')

def main():
    game_info_ajaxs('chivalrymedievalwarfare', 'C:/Users/BigData/Desktop/')
    
if __name__ == "__main__":
    main()
