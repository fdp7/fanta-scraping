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
        
        # scraping stats
        url = 'https://www.fantacalcio.it/statistiche-serie-a/' + str(season[1]) + '/italia/riepilogo'
        print(colored("\nScraping Stats of " + season[1] + " season\n",'green'))
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')        
        stats_dictionary = scrape_stats(soup)

        # scraping costs
        url = 'https://www.fantacalcio.it/quotazioni-fantacalcio/' + str(season[1])
        print(colored("\nScraping Costs of " + season[1] + " season\n",'green'))
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        cost_dictionary = scrape_costs(soup)
        
        # save stats
        save(season, stats_dictionary, cost_dictionary)

# Stats scraping
def scrape_stats(soup):
    
    # prepare dictionary
    stats_dictionary = {'name':[], 'role':[], 'team':[], 'game':[], 'mv':[], 'fm':[], 'gol':[],
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
        stats_dictionary['name'].append(name)
        stats_dictionary['role'].append(role)
        stats_dictionary['team'].append(team)
        stats_dictionary['game'].append(game)
        stats_dictionary['mv'].append(mv)
        stats_dictionary['fm'].append(fm)
        stats_dictionary['gol'].append(gol)
        stats_dictionary['gs'].append(gs)
        stats_dictionary['rig'].append(rig)
        stats_dictionary['rp'].append(rp)
        stats_dictionary['ass'].append(ass)
        stats_dictionary['amm'].append(amm)
        stats_dictionary['esp'].append(esp)

    return stats_dictionary

def scrape_costs(soup):
    # prepare dictionary
    cost_dictionary = {'name':[], 'qa':[], 'expected_cost_1000':[]}
    
    # scrape stats
    for row in soup.findAll('table')[0].tbody.findAll('tr'):
        name = row.findAll('th')[3].find(class_="player-name").text.strip()
        qa = row.find(class_="player-classic-current-price").text.strip()
        expected_cost_1000 = row.find(class_="player-classic-fvm").text.strip()
        #if expected_cost_1000 == "-":
        #    expected_cost_1000 = "1"

        # save to dictionary
        cost_dictionary['name'].append(name)
        cost_dictionary['qa'].append(qa)
        cost_dictionary['expected_cost_1000'].append(expected_cost_1000)

    return cost_dictionary

# Save stats to csv
def save(season, stats_dictionary, cost_dictionary):
    
    # create data frame
    df_player = pd.DataFrame({'Calciatore':stats_dictionary['name'],
                    'Ruolo':stats_dictionary['role'],
                    'Squadra':stats_dictionary['team'],
                    'Partite Giocate':stats_dictionary['game'],
                    'MV':stats_dictionary['mv'],
                    'FM':stats_dictionary['fm'],
                    'Gol':stats_dictionary['gol'],
                    'Gol Subiti':stats_dictionary['gs'],
                    'Rigori':stats_dictionary['rig'],
                    'Rigori Parati':stats_dictionary['rp'],
                    'Assist':stats_dictionary['ass'],
                    'Ammonizioni':stats_dictionary['amm'],
                    'Espulsioni':stats_dictionary['esp']})

    df_cost = pd.DataFrame({'Calciatore':cost_dictionary['name'],
                    'QA':cost_dictionary['qa'],
                    'ExpectedCost_1000':cost_dictionary['expected_cost_1000']})
    
    df = df_player.merge(df_cost, how="left", on="Calciatore")
    print(df.head()) 

    # create folder and save                    
    filepath = str(season[1])
    os.makedirs(filepath, exist_ok=True) 
    filename = filepath + '/' + filepath + '.csv'
    df.to_csv(filename)


# ------------------- MAIN ------------------- #

seasons = get_seasons()
get_players_stats(seasons)