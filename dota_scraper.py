# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 17:35:10 2019

@author: Charles Edmond TanYZ
"""

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import unicodedata

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
all_hrefs = []
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

all_hrefs.append(str_hrefs)
all_hrefs.append(agi_hrefs)
all_hrefs.append(int_hrefs)

names = []
pri_attrs = []

base_str = []
str_gain = []
base_agi = []
agi_gain = []
base_int = []
int_gain = []

base_healths = []
base_hp_regens = []
base_mag_reses = []
base_manas = []
base_mana_regens = []
base_spell_dmgs = []
base_armors = []
base_att_per_secs = []
base_move_speed_amps = []
#base_dmg_mins = []
#base_dmg_maxs = []
base_dmgs = []

movement_speeds = []
turn_rates = []
vision_days = []
vision_nights = []
attack_ranges = []
projectile_speeds = []
attack_points = []
backswings = []
base_attack_times = []
collision_sizes = []
legss = []


for i in range(len(all_hrefs)):
    for href in all_hrefs[i]:
        if i == 0:
            pri_attrs.append('Strength')
        elif i == 1:
            pri_attrs.append('Agility')
        elif i == 2:
            pri_attrs.append('Intelligence')
        
        
        url = 'https://dota2.gamepedia.com'+href
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        global_wrapper = soup.find('div', id='global-wrapper')
        page_wrapper = global_wrapper.find('div', id='pageWrapper')
        content = page_wrapper.find('div', id='content')
        
        name = content.find('h1', itemprop='name').text
        print('Scraping hero: ' + name)
        names.append(name)

        
        bodyContent = content.find('div', id='bodyContent')
        mw_content_text = bodyContent.find('div', id='mw-content-text')
        mw_parser_output = mw_content_text.find('div', class_='mw-parser-output')
        table = mw_parser_output.find('table', class_='infobox')
        table_body = table.find('tbody')
        trs = table_body.find_all('tr')
        
        # for attributes
        attr_tr = trs[2]
        attr_div = attr_tr.find('div')
        attr_strs = attr_div.find_all('div')
        
        str_s = attr_strs[3].text
        base_str.append(str_s.split(' ')[0])
        str_gain.append(str_s.split(' ')[2])
        
        agi_s = attr_strs[4].text
        base_agi.append(agi_s.split(' ')[0])
        agi_gain.append(agi_s.split(' ')[2])
        
        int_s = attr_strs[5].text
        base_int.append(int_s.split(' ')[0])
        int_gain.append(int_s.split(' ')[2])
        
        # for properties: like health regen, etc
        prop_tr = trs[3]
        prop_table = prop_tr.find('table', class_='evenrowsgray')
        prop_table_body = prop_table.find('tbody')
        prop_trs = prop_table_body.find_all('tr')
        
        health_tr = prop_trs[1]
        base_health = health_tr.find('td').text
        base_healths.append(base_health)
        
        hp_regen_tr = prop_trs[2]
        base_hp_regen = hp_regen_tr.find('td').text
        base_hp_regens.append(base_hp_regen)
        
        mag_res_tr = prop_trs[3]
        base_mag_res = mag_res_tr.find('td').text
        base_mag_reses.append(base_mag_res)
    
        mana_tr = prop_trs[4]
        base_mana = mana_tr.find('td').text
        base_manas.append(base_mana)
    
        mana_regen_tr = prop_trs[5]
        base_mana_regen = mana_regen_tr.find('td').text
        base_mana_regens.append(base_mana_regen)
        
        spell_dmg_tr = prop_trs[6]
        base_spell_dmg = spell_dmg_tr.find('td').text
        base_spell_dmgs.append(base_spell_dmg)
        
        armor_tr = prop_trs[7]
        base_armor = armor_tr.find('td').text
        base_armors.append(base_armor)
        
        att_per_sec_tr = prop_trs[8]
        base_att_per_sec = att_per_sec_tr.find('td').text
        base_att_per_secs.append(base_att_per_sec)
        
        move_speed_amp_tr = prop_trs[9]
        base_move_speed_amp = move_speed_amp_tr.find('td').text
        base_move_speed_amps.append(base_move_speed_amp)
        
        dmg_tr = prop_trs[10]
        base_dmg = dmg_tr.find('td').text.encode('utf-8')
#        base_dmg_min = base_dmg.split('-')[0]
#        base_dmg_max = base_dmg.split('-')[1]
#        base_dmg_mins.append(base_dmg_min)
#        base_dmg_maxs.append(base_dmg_max)
        base_dmgs.append(base_dmg)
        
        
        # more properties, movespeed, etc

        prop2_table = table_body.find('table', class_='oddrowsgray')
        prop2_tbody = prop2_table.find('tbody')
        prop2_trs = prop2_tbody.find_all('tr')
        
        movement_speed_tr = prop2_trs[0]
        movement_speed = movement_speed_tr.find('td').text
        movement_speeds.append(movement_speed)
        
        turn_rate_tr = prop2_trs[1]
        turn_rate = turn_rate_tr.find('td').text
        turn_rates.append(turn_rate)
        
        vision_tr = prop2_trs[2]
        vision = vision_tr.find('td').text
        vision_day = vision.split('/')[0]
        vision_night = vision.split('/')[1]
        vision_days.append(vision_day)
        vision_nights.append(vision_night)
        
        attack_range_tr = prop2_trs[3]
        attack_range = attack_range_tr.find('td').text
        attack_ranges.append(attack_range)
        
        projectile_speed_tr = prop2_trs[4]
        projectile_speed = projectile_speed_tr.find('td').text
        projectile_speeds.append(projectile_speed)
        
        attack_animation_tr = prop2_trs[5]
        attack_animation = attack_animation_tr.find('td').text
        attack_point = attack_animation.split('+')[0]
        backswing = attack_animation.split('+')[1]
        attack_points.append(attack_point)
        backswings.append(backswing)
        
        base_attack_time_tr = prop2_trs[6]
        base_attack_time = base_attack_time_tr.find('td').text
        base_attack_times.append(base_attack_time)
        
        collision_size_tr = prop2_trs[7]
        collision_size = collision_size_tr.find('td').text
        collision_sizes.append(collision_size)
        
        legs_tr = prop2_trs[8]
        legs = legs_tr.find('td').text.encode('utf-8')
        legss.append(legs)
        
df = pd.DataFrame({'Names': names,
                   'Primary Attribute': pri_attrs,
                   'Base Strength': base_str,
                   'Strength Gain': str_gain,
                   'Base Agility': base_agi,
                   'Agility Gain': agi_gain,
                   'Base Intelligence': base_int,
                   'Intelligence Gain': int_gain,
                   'Base Health': base_healths,
                   'Base HP Regeneration': base_hp_regens,
                   'Base Magic Resistance': base_mag_reses,
                   'Base Mana': base_manas,
                   'Base Mana Regeneration': base_mana_regens,
                   'Base Spell Damage Amplification': base_spell_dmgs,
                   'Base Armor': base_armors,
                   'Base Attacks per Second': base_att_per_secs,
                   'Base Movement Speed Amplification': base_move_speed_amps,
                   'Base Damage': base_dmgs,
#                   'Base Min Damage': base_dmg_mins,
#                   'Base Max Damage': base_dmg_maxs,
                   'Base Movement Speed': movement_speeds,
                   'Turn Rate': turn_rates,
                   'Day Vision': vision_days,
                   'Night Vision': vision_nights,
                   'Attack Range': attack_ranges,
                   'Projectile Speed': projectile_speeds,
                   'Attack Point': attack_points,
                   'Attack Backswing': backswings,
                   'Base Attack Time': base_attack_times,
                   'Collision Size': collision_sizes,})
    
df = df[['Names', 'Primary Attribute', 'Base Strength', 'Strength Gain', 'Base Agility', 'Agility Gain',
         'Base Intelligence', 'Intelligence Gain', 'Base Health', 'Base HP Regeneration',
         'Base Magic Resistance', 'Base Mana', 'Base Mana Regeneration',
         'Base Spell Damage Amplification', 'Base Armor', 'Base Attacks per Second',
         'Base Movement Speed Amplification', 'Base Damage',
         'Base Movement Speed', 'Turn Rate', 'Day Vision', 'Night Vision',
         'Attack Range', 'Projectile Speed', 'Attack Point', 'Attack Backswing',
         'Base Attack Time', 'Collision Size']]

df.to_csv('Dota Heroes Stats.csv', encoding = 'utf-8', index = False)

