# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:35:10 2019

@author: Charles Edmond TanYZ
"""

from bs4 import BeautifulSoup
from requests import get
import pandas as pd

# get links to each hero
# so we can loop through each link and get info for each hero

hero_list_url = 'https://dota2.gamepedia.com/Heroes'
response = get(hero_list_url)
html_soup = BeautifulSoup(response.text, 'html.parser')

global_wrapper = html_soup.find('div', id='global-wrapper')
page_wrapper = global_wrapper.find('div', id='pageWrapper')
content = page_wrapper.find('div', id='content')
bodyContent = content.find('div', id='bodyContent')
mw_content_text = bodyContent.find('div', id='mw-content-text')
mw_parser_output = mw_content_text.find('div', class_='mw-parser-output')
main_table = mw_parser_output.find('table')
table_body = main_table.find('tbody')
tables = table_body.find_all('tr')

str_hrefs = []
agi_hrefs = []
int_hrefs = []

# strength heroes
strength_heroes_table = tables[1].find('td')
#strength_heroes = strength_heroes_table.find_all('div')
for hero in strength_heroes_table:
    try:
        str_hrefs.append(hero.find('a')['href'])
    except TypeError:
        pass
agility_heroes_table = tables[3].find('td')
for hero in agility_heroes_table:
    try:
        agi_hrefs.append(hero.find('a')['href'])
    except TypeError:
        pass
int_heroes_table = tables[5].find('td')
for hero in int_heroes_table:
    try:
        int_hrefs.append(hero.find('a')['href'])
    except TypeError:
        pass

for href in str_hrefs:
    url = 'https://dota2.gamepedia.com'+href
    print(url)