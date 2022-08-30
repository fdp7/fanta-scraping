import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
from termcolor import colored


# Get seasons
def get_seasons():
    
    url = 'https://www.fantacalcio.it/statistiche-serie-a'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    seasons_list = soup.find(class_='filters mt-3 mb-2')
    seasons_list = seasons_list.find(attrs={'id':'season'})
    seasons_list = seasons_list.find_all('option')

    seasons = np.array('Seasons')
    for season in seasons_list:
        seasons = np.append(seasons,season)
    seasons = np.sort(seasons)[::-1]

    return seasons


# Get stats for each player for each season
def get_players_stats(seasons):

    for season in seasons[0:len(seasons)-1]:
        
        # rename season 
        season = season.replace('/','-').split()
        
        # shuffle headers
        ua = UserAgent()
        ua.update()
        headers = {'User-Agent': ua.random}
        
        # connect to page
        url = 'https://www.fantacalcio.it/statistiche-serie-a/' + str(season[1]) + '/italia/riepilogo'
        print(colored("\nScraping " + season[1] + " season\n",'green'))
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # make scraping
        player_dictionary = scrape(soup)
        
        # save stats
        save_stats(season, player_dictionary)


# Stats scraping
def scrape(soup):
    
    # prepare dictionary
    player_dictionary = {'name':[], 'role':[], 'team':[], 'game':[], 'mv':[], 'fm':[], 'gol':[],
        'gs':[], 'rig':[], 'rp':[], 'ass':[], 'amm':[], 'esp':[]}
    
    # scrape stats
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        role = row.findAll('th')[1].find(class_="role")['data-value'].strip()
        name = row.findAll('th')[3].find('a').text.strip()
        team = row.findAll('td')[0].text.strip()
        game = row.findAll('td')[1].text.strip()
        mv = row.findAll('td')[2].text.strip()
        fm = row.findAll('td')[3].text.strip()
        gol = row.findAll('td')[4].text.strip()
        gs = row.findAll('td')[5].text.strip()
        rig = row.findAll('td')[6].text.strip()
        rp = row.findAll('td')[7].text.strip()
        ass = row.findAll('td')[8].text.strip()
        amm = row.findAll('td')[9].text.strip()
        esp = row.findAll('td')[10].text.strip()

        # save to dictionary
        player_dictionary['name'].append(name)
        player_dictionary['role'].append(role)
        player_dictionary['team'].append(team)
        player_dictionary['game'].append(game)
        player_dictionary['mv'].append(mv)
        player_dictionary['fm'].append(fm)
        player_dictionary['gol'].append(gol)
        player_dictionary['gs'].append(gs)
        player_dictionary['rig'].append(rig)
        player_dictionary['rp'].append(rp)
        player_dictionary['ass'].append(ass)
        player_dictionary['amm'].append(amm)
        player_dictionary['esp'].append(esp)

    return player_dictionary


# Save stats to csv
def save_stats(season, player_dictionary):
    
    # create data frame
    Data_frame = pd.DataFrame({'Calciatore':player_dictionary['name'],
                    'Ruolo':player_dictionary['role'],
                    'Squadra':player_dictionary['team'],
                    'Partite Giocate':player_dictionary['game'],
                    'MV':player_dictionary['mv'],
                    'FM':player_dictionary['fm'],
                    'Gol':player_dictionary['gol'],
                    'Gol Subiti':player_dictionary['gs'],
                    'Rigori':player_dictionary['rig'],
                    'Rigori Parati':player_dictionary['rp'],
                    'Assist':player_dictionary['ass'],
                    'Ammonizioni':player_dictionary['amm'],
                    'Espulsioni':player_dictionary['esp']})

    # create folder and save                    
    filepath = str(season[1])
    os.makedirs(filepath, exist_ok=True) 
    filename = filepath + '/' + filepath + '.csv'
    Data_frame.to_csv(filename)


# ------------------- MAIN ------------------- #

seasons = get_seasons()
get_players_stats(seasons)